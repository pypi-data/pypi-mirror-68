# Copyright Netflix, 2019
import json
from logging import getLogger
from typing import Any
from typing import Dict
from typing import Optional
from typing import Text

# Implementation libs
from kaiju_mqtt_py.kaiju_mqtt_py import KaijuMqtt

from .retry_with_backoff import retry

logger = getLogger(__name__)


class MqttRetryableError(Exception):
    pass


class DeviceIdentifier:
    """
    Identify a device to the ADB module with an IP, a serial number, or an ESN.
    """

    def __init__(self, **kwargs):
        """Constructor."""
        self.esn = kwargs.get("esn", None)
        self.ip = kwargs.get("ip", None)
        self.serial = kwargs.get("serial", None)

    def as_dict(self) -> Dict:
        """
        Get the dict representation of this identifier.

        If there is no valid value set, raise a ValueError.
        :return:
        """
        if self.esn is not None:
            return {"device_esn": self.esn}

        elif self.ip is not None:
            return {"device_ip": self.ip}

        elif self.serial is not None:
            return {"device_serial": self.serial}

        else:
            raise ValueError("No device identifier was set.")

    def as_json(self) -> Text:
        """
        Get the json serialized representation of this as a string.

        :return:
        """
        return json.dumps(self.as_dict())

    @staticmethod
    def sanity_check(id: Dict) -> bool:
        """
        Perform a basic sanity check on a dict to see if it contains an identifier.

        Note that the value of the identifier is not checked, even for formatting.

        :param id:
        :return:
        """
        return (
            "target" in id
            or "device_esn" in id
            or "device_serial" in id
            or "device_ip" in id
        )


class Request:
    """
    Check the format of a request to the ADB module over the MQTT bus.

    Note that this class used to be bigger and now this is all that's left.
    """

    @staticmethod
    def sanity_check(plan: Dict) -> bool:
        """Perform a basic sanity check on a dict to see if it's mostly the right shape for a request."""
        results = [DeviceIdentifier.sanity_check(plan)]

        try:
            if "testplan" in plan:
                results.append("testcases" in plan["testplan"])
                results.append(type(plan["testplan"]["testcases"]) is list)
                results.append(len(plan["testplan"]["testcases"]) > 0)
        except KeyError:
            results.append(False)
        except TypeError:
            results.append(False)
        except ValueError:
            results.append(False)

        return all(results)


class Session:
    """
    A connection to remote MQTT brokers for running tests.

    This object only tracks state surrounding the KaijuMqtt connection.
    """

    automation_status_topic_pattern = "test_runner/{}"

    def __init__(self):
        """Constructor."""
        self.kaiju = KaijuMqtt()
        self.status = {}
        self.cleanup_funcs = []

    def connect(self, broker: Text, port: int) -> None:
        """
        Connect the underlying broker.

        The client should explicitly call mysession.destructor() to clean up.

        :param broker: The host/ip to connect to.
        :param port: The port to connect to. The normal default is 1883, but this is not set by default.
        :return: None
        """
        self.kaiju.connect(broker, port)

    def subscribe(self, topic: Text, newfunc: Any, options_dict: Dict = None) -> None:
        """
        Subscribe to a topic with the underlying MQTT broker.

        This typically would be used to subscribe to the status of a test plan.

        The signature of the new function should be:
        def handle_updates(client, userdata, packet):
            ...

        This is the normal shape for a paho-mqtt topic message subscriber. The most interesting arg is packet.payload,
        of type dict. The packet.payload is a list of dicts. The dicts start out with the following keys:
        url, status, name logfile, step
        These will be populated with the current state of the test run. This will get called typically whenever one of
        the elements changes its value in the ADB module.

        :param topic:
        :param newfunc:
        :param options_dict:
        :return:
        """
        options = options_dict if options_dict else {"qos": 1, "timeoutMs": 15000}
        # todo v. short on exception/error handling here
        cleanup = self.kaiju.subscribe(topic, newfunc, options)

        self.cleanup_funcs.append(cleanup)

    def get_test_plan_for_device(self, device: DeviceIdentifier) -> Dict:
        """
        Request a test plan from the remote server.

        This is returned as a JSON dict.

        Example response:
        {"branch": "5.1",
        "testcases": [
                {"exec": "/tests/suite/file1.js?args"},
                {"exec": "/tests/suite/file2.js?args"},
                ...
            ],
        "sdkVersion": "ninja_6",
        }


        To run this plan, it needs to be put in the following structure:
        { "device_ip": "some_ip",
          "testplan" : <this object> }

        :param device: The DeviceIdentifier to use in the data section of the request.
        :return: The response from the ADB module as a dict.
        """
        response = self.kaiju.request(
            Session.automation_status_topic_pattern.format("get_testplan"),
            device.as_dict(),
            options={"qos": 2, "timeoutMs": 3 * 60 * 1000},
        )
        return response

    @retry((MqttRetryableError,))
    def run_plan(self, plan) -> Dict:
        """
        Send a request to run a specified test plan.

        This will do a basic sanity check on the test plan for general shape before submitting, because I am a terrible
        typist. If there is a problem with the plan's format, SyntaxError will be raised.

        A request needs to be formed around the results of a call to get_test_plan_for_device before
        calling this. It should be shaped like this:
        { "device_ip": "some_ip",
          "testplan" : <test plan object from get_test_plan_for_device>}


        The plan will get a basic sanity check before being sent on. Errors will be surfaced as SyntaxError.

        :param plan: The plan to execute.
        :return: The response from the ADB module as a dict.
        """
        if not Request.sanity_check(plan):
            logger.critical("The request failed basic sanity checks.")
            raise SyntaxError("The request failed basic sanity checks.")
        response = self.kaiju.request(
            Session.automation_status_topic_pattern.format("run_tests"),
            plan,
            {"qos": 1, "timeoutMs": 60 * 1000},
        )
        if (
            "body" in response
            and "message" in response["body"]
            and "Device is currently busy" in response["body"]["message"]
        ):
            # busy message looks similar to this:
            # {'status': 200,
            # 'body': {'status': 'running', 'message':
            #          'Device is currently busy running tests, request test cancellation or try again later'}}

            if "device_ip" in plan:
                requested_device = DeviceIdentifier(ip=plan["device_ip"])
            elif "device_esn" in plan:
                requested_device = DeviceIdentifier(esn=plan["device_esn"])
            elif "device_serial" in plan:
                requested_device = DeviceIdentifier(serial=plan["device_serial"])
            self.cancel_plan_for_device(requested_device)
            raise MqttRetryableError(
                "The device thinks it was busy. Requesting a cancel of the current run."
            )

        return response

    def cancel_plan_for_device(self, device) -> Dict:
        """
        Request that we cancel the tests for this device.

        :param device: Which device to cancel for.
        :return: dict with keys status and body. Status will be a typical HTTP error code.
        """
        response = self.kaiju.request(
            Session.automation_status_topic_pattern.format("cancel_tests"),
            device.as_dict(),
        )
        return response

    def destructor(self):
        """
        Cleanly shut down the KaijuMqtt object and disconnect.

        Some unsubscribe actions need to be performed on shutdown of the client. I'd suggest putting this in a finally:
        clause to prevent strange behaviors. It is safe to call this multiple times.

        :return:
        """
        [x() for x in self.cleanup_funcs]
        self.kaiju.close()


class StatefulSession:
    """
    A simplified client that handles most of the boilerplate of monitoring testing.

    This object handles state of the connection to a KaijuMqtt agent, the device, and the test plan.

    This object also simplifies getting status updates. Any object that implements "handle_progress_update(payload)" and
    "handle_run_complete(packet)" can be appended to this.status_watchers to get updates as the run progresses.
    """

    def __init__(self, **kwargs):
        """
        Construct a new StatefulSession. Args are passed to the DeviceIdentifier constructor.

        :param kwargs: Passed unmodified to the DeviceIdentifier constructor. ex: esn=DEVICE_12345 or ip=192.168.144.49
        """
        self.connected: bool = False
        self.device: DeviceIdentifier = DeviceIdentifier(**kwargs)
        self.plan_request: Optional[Dict] = None
        self.session: Session = Session()
        self.status_watchers = []

    def connect(self, broker: Text, port: int):
        """Connect the session to an MQTT broker."""
        self.session.connect(broker, port)
        self.connected = True

    def get_test_plan(self):
        """Get the test plan and store it internally."""
        plan_response = self.session.get_test_plan_for_device(self.device)
        if "status" in plan_response and plan_response["status"] != 200:
            raise ValueError("Getting the test plan failed with a bad status code.")
        if (
            "body" not in plan_response
            or "testcases" not in plan_response["body"]
            or not isinstance(plan_response["body"]["testcases"], list)
            or len(plan_response["body"]["testcases"]) < 1
        ):
            msg = "The test plan was returned but did not appear valid."
            logger.error(msg)
            logger.error(plan_response)
            raise ValueError(msg)

        self.plan_request = self.device.as_dict()
        self.plan_request["testplan"] = plan_response["body"]

    def run_tests(self):
        """Start the test plan and update watchers in the status_watchers list."""
        if self.plan_request is None:
            self.get_test_plan()

        def receive_update(client, userdata, packet):
            """
            Broadcast received updates to watchers.

            :param client:
            :param userdata:
            :param packet:
            :return:
            """

            [
                watcher.handle_progress_update(packet.payload["results"])
                for watcher in self.status_watchers
            ]

            # we hand down the entire packet so the topic and payload can be inspected
            # when multiple devices are sending updates at once, this is how you tell which one is done during reporting
            if "running" in packet.payload and not packet.payload["running"]:
                [
                    watcher.handle_run_complete(packet)
                    for watcher in self.status_watchers
                ]

        full_result = self.session.run_plan(self.plan_request)
        if full_result["status"] != 200:
            logger.error("The test plan run was not run:")
            logger.error(full_result)

        if (
            full_result is None
            or "body" not in full_result
            or "resultTopic" not in full_result["body"]
        ):
            logger.error("The test plan run got a malformed response")
            logger.error(full_result)
        else:
            # Subscribe to topic returned as “resultTopic” to get test result stream
            self.session.subscribe(full_result["body"]["resultTopic"], receive_update)

    def cancel(self):
        self.session.cancel_plan_for_device(self.device)

    def close(self):
        self.session.destructor()
