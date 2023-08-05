# Copyright Netflix, 2019
import logging
import signal
import sys
from threading import Event

import click

# Implementation libs
import runez
from paho.mqtt.client import Client

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
topic_list = ["test_runner/#", "expiring/#", "_response/#", "dut/#", "subservice/#"]


class MyUserData:
    def __init__(self):
        self.connected_event = Event()
        self.disconnected_event = Event()
        self.esn = ""


def on_connect(client, userdata, flags, rc):
    """Set the connected state and subscribe to existing known topics."""
    for topic in topic_list:
        client.subscribe(topic)
    userdata.connected_event.set()
    userdata.disconnected_event.clear()


def on_disconnect(client, userdata, rc):
    """Set the disconnected state."""
    userdata.connected_event.clear()
    userdata.disconnected_event.set()


def on_message(client, userdata, packet):
    """Just log anything that comes in with the timestamp we got it."""
    if packet:
        if userdata.esn != "":
            if userdata.esn in packet.topic:
                logging.info("topic: " + packet.topic)
                logging.info("payload: " + str(packet.payload))
        else:
            logging.info("topic: " + packet.topic)
            logging.info("payload: " + str(packet.payload))


@runez.click.command()
@runez.click.version()
@click.option("--esn", type=str, envvar="ESN", help="An string to filter topics with.")
@click.option(
    "--rae",
    type=str,
    envvar="RAE",
    required=True,
    help="The Netflix RAE device to connect to.",
)
def support(rae, esn):
    try:
        userdata = MyUserData()
        client = Client(userdata=userdata)

        def signal_handler(signal, frame):
            print("Heard exit request - cleaning up.")
            for topic_ in topic_list:
                client.unsubscribe(topic_)
            client.disconnect()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        client.enable_logger(logger)
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        client.connect(rae, 1883)
        client.loop_start()
        userdata.esn = esn if esn is not None else ""
        userdata.connected_event.wait(15.0)
        if not userdata.connected_event.is_set():
            raise Exception("Connect timed out after 15 seconds.")

        userdata.disconnected_event.wait()  # yes, forever

    finally:
        for topic in topic_list:
            client.unsubscribe(topic)
        client.disconnect()


if __name__ == "__main__":
    support()
