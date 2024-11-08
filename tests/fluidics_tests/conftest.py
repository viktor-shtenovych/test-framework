"""! @brief Configurations for Fluidics tests."""
##
# @file conftest.py
#
# @brief Configurations for Fluidics tests.
#
# @section description_conftest_fluidics Description
# This config representing configurations for Fluidics tests.
#
# @section libraries_conftest_fluidics Libraries/Modules
# - typing standard library (https://docs.python.org/3/library/typing.html)
# - pytest standard library (https://pypi.org/project/pytest/)
# - reports module (local)
# - common_fixtures module (local)
# - fluidics_simulator module (local)
#   - Access to FluidicsSimulator class.
# - fluidics module (local)
#   - Access to Fluidics class.
#
# @section notes_conftest_fluidics Notes
# - None.
#
# @section todo_conftest_fluidics TODO
# - None.
#
# @section author_conftest_fluidics Author(s)
# - Created by:
#   - Maksym Masalov <maksym.masalov@globallogic.com> on 06/09/2024.
# - Modified by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 09/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic.  All rights reserved.

from typing import Iterator

import pytest
import _pytest.fixtures

from framework.simulators.fluidics_simulator import FluidicsSimulator
from framework.apps.fluidics import Fluidics
from framework.support.reports import logger

from tests.common.common_fixtures import create_simulator, create_emulator

pytest_plugins = ["tests.plugins.hooks"]


@pytest.fixture(scope="function")
def simulator(
    request: _pytest.fixtures.FixtureRequest,
) -> Iterator[FluidicsSimulator]:
    """! Create a simulator."""
    yield from create_simulator(request, FluidicsSimulator)


@pytest.fixture(scope="function")
def fluidics(simulator: FluidicsSimulator) -> Iterator[Fluidics]:
    """! Create a fluidics module."""
    fluidics = Fluidics.create_from_sim(simulator)
    fluidics.vtime.sleep(0.370)
    logger.info("Emulator initialization is expected to be done")
    yield fluidics


@pytest.fixture(scope="function", autouse=True)
def emulator(
    request: _pytest.fixtures.FixtureRequest, simulator: FluidicsSimulator
) -> Iterator[None]:
    """! Create an emulator."""
    yield from create_emulator(request, simulator)
