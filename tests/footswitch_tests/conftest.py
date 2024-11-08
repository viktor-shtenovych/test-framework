from typing import Iterator

import pytest
import _pytest.fixtures

from framework.simulators.footswitch_simulator import FootSwitchSimulator
from framework.apps.footswitch import FootSwitch
from framework.support.reports import logger

from tests.common.common_fixtures import create_simulator, create_emulator

pytest_plugins = ["tests.plugins.hooks"]


@pytest.fixture(scope="function")
def simulator(
    request: _pytest.fixtures.FixtureRequest,
) -> Iterator[FootSwitchSimulator]:
    """
    Create a simulator.
    """
    yield from create_simulator(request, FootSwitchSimulator)


@pytest.fixture(scope="function")
def foot_switch(simulator: FootSwitchSimulator) -> Iterator[FootSwitch]:
    """
    Create a footswitch.
    """
    foot_switch = FootSwitch.create_from_sim(simulator)
    foot_switch.vtime.sleep(0.370)
    logger.info("Emulator initialization is expected to be done")
    yield foot_switch
    foot_switch.wired_conn.disable_beacons()


@pytest.fixture(scope="function", autouse=True)
def emulator(
    request: _pytest.fixtures.FixtureRequest, simulator: FootSwitchSimulator
) -> Iterator[None]:
    """
    Create an emulator.
    """
    yield from create_emulator(request, simulator)
