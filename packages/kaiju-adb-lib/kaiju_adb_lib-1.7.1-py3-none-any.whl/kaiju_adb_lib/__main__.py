#!/usr/bin/env python
"""
This docstring will appear as epilog of your --help
"""
# Copyright Netflix, 2019
import json
import signal
import sys
from contextlib import contextmanager
from threading import Event
from typing import Generator

import click

# Implementation libs
import runez

from .client import StatefulSession


# ================================================================================
def make_basic_options_dict(esn, ip, rae, serial):
    """Make the boilerplate "form my options dict" go away."""

    options = {"rae": rae}
    if esn is not None:
        options["esn"] = esn
    if ip is not None:
        options["ip"] = ip
    if serial is not None:
        options["serial"] = serial
    return options


# ================================================================================
@contextmanager
def stateful_session_mgr(**kwargs) -> Generator[StatefulSession, None, None]:
    """Yield and clean up after a stateful session manager."""

    try:
        session = StatefulSession(**kwargs)
        if "rae" not in kwargs:
            raise ValueError(
                "The stateful session manager call needs the keyword 'rae'."
            )
        session.connect(
            kwargs["rae"], 1883
        )  # we really don't have an alternate port, but you get it
        yield session
    finally:
        session.close()


class DoneWaitingClass:
    """Provide the hooks to wait on for background tasks."""

    def __init__(self):
        self.finished = Event()
        self.last_heard = {}

    def handle_progress_update(self, full_payload):
        self.last_heard = full_payload

    def handle_run_complete(self, packet):
        print(json.dumps(self.last_heard))
        self.finished.set()


# ================================================================================
@runez.click.command()
@runez.click.version()
@click.option(
    "--rae",
    type=str,
    required=True,
    help="The Netflix RAE device to connect to.",
    envvar="RAE",
)
@click.option(
    "--esn",
    type=str,
    help="The ESN of the target device. Mutually exclusive to ip and serial.",
    envvar="ESN",
)
@click.option(
    "--ip",
    type=str,
    help="The IP address of the target device. Mutually exclusive to esn and serial.",
    envvar="DUT_IP",
)
@click.option(
    "--serial",
    type=str,
    help="The serial number of the target device. Mutually exclusive to ip  and esn.",
    envvar="DUT_SERIAL",
)
@click.option(
    "--testplan",
    type=click.File("w"),
    required=True,
    help="The file to write the test plan to.",
)
@click.option("--debug", is_flag=True, help="Show debugging information.")
@click.option("--log", is_flag=True, help="Log to file at given location.")
@runez.click.log()
def get_plan_from_device(debug, log, rae, esn, ip, serial, testplan):
    """
    Run the test on the device that retreives and decodes a test plan as json.
    """
    runez.log.setup(
        debug=debug, file_location=log, locations=None, greetings=":: {argv}"
    )

    options = make_basic_options_dict(esn, ip, rae, serial)

    with stateful_session_mgr(**options) as session:

        def signal_handler(signal, frame):
            print("Heard cancel request - asking the control module to cancel tests.")
            session.cancel()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        session.get_test_plan()  # reminder: stored in the session object at session.plan_request

        json.dump(session.plan_request, testplan)


# ================================================================================
@runez.click.command()
@runez.click.version()
@click.option(
    "--rae",
    type=str,
    required=True,
    help="The Netflix RAE device to connect to.",
    envvar="RAE",
)
@click.option(
    "--esn",
    type=str,
    help="The ESN of the target device. Mutually exclusive to ip and serial.",
    envvar="ESN",
)
@click.option(
    "--ip",
    type=str,
    help="The IP address of the target device. Mutually exclusive to esn and serial.",
    envvar="DUT_IP",
)
@click.option(
    "--serial",
    type=str,
    help="The serial number of the target device. Mutually exclusive to ip  and esn.",
    envvar="DUT_SERIAL",
)
@click.option("--debug", is_flag=True, help="Show debugging information.")
@click.option("--log", is_flag=True, help="Log to file at given location.")
@runez.click.log()
def cancel_session_on_device(debug, log, rae, esn, ip, serial):
    """
    Cancel any pending tests for a specified device.
    """
    runez.log.setup(
        debug=debug, file_location=log, locations=None, greetings=":: {argv}"
    )

    options = make_basic_options_dict(esn, ip, rae, serial)

    with stateful_session_mgr(**options) as session:

        def signal_handler(signal, frame):
            print("Heard cancel request - asking the control module to cancel tests.")
            session.cancel()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        session.cancel()


# ================================================================================
@runez.click.command()
@runez.click.version()
@click.option(
    "--rae",
    type=str,
    required=True,
    help="The Netflix RAE device to connect to.",
    envvar="RAE",
)
@click.option(
    "--esn",
    type=str,
    help="The ESN of the target device. Mutually exclusive to ip and serial.",
    envvar="ESN",
)
@click.option(
    "--ip",
    type=str,
    help="The IP address of the target device. Mutually exclusive to esn and serial.",
    envvar="DUT_IP",
)
@click.option(
    "--serial",
    type=str,
    help="The serial number of the target device. Mutually exclusive to ip  and esn.",
    envvar="DUT_SERIAL",
)
@click.option(
    "--wait/--no-wait",
    default=True,
    help="Should this process block until tests are done?",
)
@click.option("--debug", is_flag=True, help="Show debugging information.")
@click.option("--log", is_flag=True, help="Log to file at given location.")
@click.option(
    "--testplan", type=click.File("rb"), help="JSON formatted test plan file."
)
@click.option(
    "--cancel", is_flag=True, help="Cancel any pending run instead of starting tests."
)
@runez.click.log()
def main(debug, log, rae, esn, ip, serial, wait, testplan, cancel):
    """
    Run a default or custom test plan on a device.

    Meant as sample or troubleshooting code, not as a full featured tool.
    """
    runez.log.setup(
        debug=debug, file_location=log, locations=None, greetings=":: {argv}"
    )

    options = make_basic_options_dict(esn, ip, rae, serial)

    chosen_plan = json.load(testplan) if testplan else None

    waiter = None

    with stateful_session_mgr(**options) as session:

        def signal_handler(signal, frame):
            print("Heard cancel request - asking the control module to cancel tests.")
            session.cancel()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        if cancel:
            session.cancel()

        if chosen_plan is not None:
            session.plan_request = chosen_plan

        if wait:
            waiter = DoneWaitingClass()
            session.status_watchers.append(waiter)

        session.run_tests()

        if wait:
            waiter.finished.wait()
