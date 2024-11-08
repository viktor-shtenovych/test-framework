"""! @brief Defines the Fluidics interface."""
##
# @file fluidics.py
#
# @brief Defines the Fluidics interface.
#
# @section description_fluidics Description
# This module represents the Fluidics class.
#
# @section libraries_fluidics Libraries/Modules
# - typing standard library (https://docs.python.org/3/library/typing.html)
# - FluidicsSimulator module (local)
#   - Access to FluidicsSimulator class.
# - FluidicsCan module (local)
#   - Access to FluidicsCan class.
#
# @section notes_fluidics Notes
# - None.
#
# @section todo_fluidics TODO
# - None.
#
# @section author_fluidics Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 10/07/2024.
# - Modified by:
#   - Maksym Masalov maksym.masalov@globallogic.com on 12/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.

from typing import Optional

from framework.core.boards.flu.buttons import FluButtons
from framework.core.boards.flu.hw_board import HwBoard
from framework.simulators.fluidics_simulator import FluidicsSimulator
from framework.communications.uvcs_fluidics.fluidics_can import FluidicsCan

from framework.hardware_interfaces.drivers.common.async_interface_driver import (
    AsyncInterfaceDriver,
)
from framework.support.reports import logger
from framework.support.vtime import vtime_manager


class Fluidics:
    """! Integration of all Fluidics functions - interface for test cases."""

    sim: Optional[FluidicsSimulator] = None

    def __init__(
        self,
        wired_conn: FluidicsCan,
        buttons: FluButtons,
        board: HwBoard,
        modem: AsyncInterfaceDriver,
    ) -> None:
        self.wired_conn = wired_conn
        self.buttons = buttons
        self._board = board
        self.vtime = vtime_manager
        self.modem = modem

    def connect(self) -> None:
        """! Connects the Fluidics to the power source."""
        logger.debug("Connecting Fluidics to the power source.")

    def disconnect(self) -> None:
        """! Disconnects the Fluidics from the power source."""
        logger.debug("Disconnecting Fluidics from the power source.")

    @classmethod
    def create_from_sim(cls, sim: FluidicsSimulator) -> "Fluidics":
        """! Class method that creates a Fluidics instance from a Simulator instance.

        This method uses the components of the Simulator instance to create and return a new FootSwitch instance.
        @param sim  The Simulator instance used to create the FootSwitch.
        @return Fluidics  The newly created FootSwitch instance.
        """
        cls.sim = sim
        return cls(
            FluidicsCan(sim.can_node),
            FluButtons(sim.hw_board),
            sim.hw_board,
            sim.async_interface,
        )
