"""! @brief Defines the FlacsLgs interface."""
##
# @file flacs_lgs.py
#
# @brief Defines the FlacsLgs interface.
#
# @section description_flacs_lgs Description
# This module represents the FlacsLgs class.
#
# @section libraries_flacs_lgs Libraries/Modules
# - typing standard library (https://docs.python.org/3/library/typing.html)
# - FlacsLgsSimulator module (local)
#   - Access to FlacsLgsSimulator class.

from typing import Optional

from framework.core.boards.flu.buttons import FluButtons
from framework.core.boards.flu.hw_board import HwBoard

from framework.simulators.flacs_lgs_simulator import FlacsLgsSimulator

# Imported from Fluidics
from framework.hardware_interfaces.drivers.common.async_interface_driver import (
    AsyncInterfaceDriver,
)

from framework.support.reports import logger
from framework.support.vtime import vtime_manager


class FlacsLgs:
    """! Integration of all FlacsLgs functions - interface for test cases."""

    # Simulator
    sim: Optional[FlacsLgsSimulator] = None

    def __init__(
        self,
        buttons: FluButtons,
        board: HwBoard,
        modem: AsyncInterfaceDriver,
    ) -> None:
        self.buttons = buttons
        self._board = board
        self.vtime = vtime_manager
        self.modem = modem

    def connect(self) -> None:
        """! Connects the FlacsLgs to the power source."""
        logger.debug("Connecting FlacsLgs to the power source.")

    def disconnect(self) -> None:
        """! Disconnects the FlacsLgs from the power source."""
        logger.debug("Disconnecting FlacsLgs from the power source.")

    @classmethod
    def create_from_sim(cls, sim: FlacsLgsSimulator) -> "FlacsLgs":
        """! Class method that creates a FlacsLgs instance from a Simulator instance.

        This method uses the components of the Simulator instance to create and return a new FootSwitch instance.
        @param sim  The Simulator instance used to create the FootSwitch.
        @return FlacsLgs  The newly created FootSwitch instance.
        """
        cls.sim = sim
        return cls(
            FluButtons(sim.hw_board),
            sim.hw_board,
            sim.async_interface,
        )
