from typing import Iterator

import pytest
import _pytest.fixtures

from framework.simulators.flacs_lgs_simulator import FlacsLgsSimulator
from framework.apps.flacs_lgs import FlacsLgs
from framework.support.reports import logger

from tests.common.common_fixtures import create_simulator, create_emulator

pytest_plugins = ["tests.plugins.hooks"]


@pytest.fixture(scope="function")
def simulator(
    request: _pytest.fixtures.FixtureRequest,
) -> Iterator[FlacsLgsSimulator]:
    """! Create a simulator."""
    yield from create_simulator(request, FlacsLgsSimulator)


@pytest.fixture(scope="function")
def flacs_lgs(simulator: FlacsLgsSimulator) -> Iterator[FlacsLgs]:
    """! Create a flacs_lgs module."""
    flacs_lgs = FlacsLgs.create_from_sim(simulator)
    flacs_lgs.vtime.sleep(0.370)
    logger.info("Emulator initialization is expected to be done")
    yield flacs_lgs


@pytest.fixture(scope="function", autouse=True)
def emulator(
    request: _pytest.fixtures.FixtureRequest, simulator: FlacsLgsSimulator
) -> Iterator[None]:
    """! Create an emulator."""
    yield from create_emulator(request, simulator)
