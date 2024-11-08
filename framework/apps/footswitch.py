"""! @Brief: FootSwitch class that integrates all FootSwitch functions - interface for test cases."""

##
# @file footswitch.py
#
# @section description_footswitch Description
# This module represents the FootSwitch class.
#
# @section libraries_footswitch Libraries/Modules
# - FootSwitchCAN module (local)
#   - Access to FootSwitchCAN class.
# - Treadle module (local)
#   - Access to Treadle class.
# - FswButtons module (local)
#   - Access to FswButtons class.
# - Leds module (local)
#   - Access to Leds class.
# - HwBoard module (local)
#   - Access to HwBoard class.
# - Batteries module (local)
#   - Access to Batteries class.
# - Position module (local)
#   - Access to Position class.
# - FootSwitchSimulator module (local)
#   - Access to FootSwitchSimulator class.
# - vtime_manager module (local)
#   - Access to vtime_manager class.
# - AsyncInterfaceDriver module (local)
#   - Access to AsyncInterfaceDriver class.
#
# @section notes_footswitch Notes
# - None.
#
# @section todo_footswitch TODO
# - None.
#
# @section author_footswitch Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 10/07/2024.
# - Modified by:
#   - Maksym Masalov maksym.masalov@globallogic.com on 12/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.
from framework.communications.uvcs_footswitch.footswitch_can import FootSwitchCAN
from framework.core.components.batteries import Batteries
from framework.core.boards.fsw.buttons import FswButtons
from framework.core.components.position import Position
from framework.simulators.footswitch_simulator import FootSwitchSimulator
from framework.core.boards.fsw.hw_board import HwBoard
from framework.core.components.leds import Leds
from framework.core.components.treadle import Treadle
from framework.support.vtime import vtime_manager
from framework.hardware_interfaces.drivers.common.async_interface_driver import (
    AsyncInterfaceDriver,
)


class FootSwitch:
    """
    ! Integration of all FootSwitch functions - interface for test cases.
    """

    def __init__(
        self,
        wired_conn: FootSwitchCAN,
        treadle: Treadle,
        buttons: FswButtons,
        leds: Leds,
        board: HwBoard,
        batteries: Batteries,
        position: Position,
        modem: AsyncInterfaceDriver,
    ) -> None:
        self.wired_conn = wired_conn
        self.buttons = buttons
        self.leds = leds
        self.treadle = treadle
        self.vtime = vtime_manager
        self._board = board
        self.batteries = batteries
        self.position = position
        self.modem = modem

        self.buttons.left_vertical.release_button()
        self.buttons.left_horizontal.release_button()
        self.buttons.right_horizontal.release_button()
        self.buttons.right_vertical.release_button()
        self.buttons.left_heel.release_button()
        self.buttons.right_heel.release_button()
        self._board.broken_spring.state = False
        self.treadle.up()

        self._board.cable_in.state = False
        self._board.vchgdt.state = False
        self._board.cable_voltage.voltage = 0.0

        self._board.coil_mon.state = False  # no wireless charger
        self._board.vcoil_pg.state = False  # no wireless charger voltage
        self._board.vchgdt.state = False  # no cable or wireless charger
        self._board.bl654_tx.state = False
        self._board.bl654_ready_n.state = False  # Ready
        self._board.bl654_busy.state = False  # Ready
        self._board.pd_shroud_up2.state = True  # TODO: implement shroud detection
        self._board.pd_shroud_up1.state = True  # TODO: implement shroud detection

    def connect(self) -> None:
        """
        ! Connects the FootSwitch to the power source.

        This method sets the state of the cable_in and vchgdt attributes of the board to True,
        and sets the cable_voltage to 24.0, indicating that the FootSwitch is connected to the power source.
        """
        self._board.cable_in.state = True
        self._board.vchgdt.state = True
        self._board.cable_voltage.voltage = 24.0

    def disconnect(self) -> None:
        """
        ! Disconnects the FootSwitch from the power source.

        This method sets the state of the cable_in and vchgdt attributes of the board to False,
        and sets the cable_voltage to 0.0, indicating that the FootSwitch is disconnected from the power source.
        """
        self._board.cable_in.state = False
        self._board.vchgdt.state = False
        self._board.cable_voltage.voltage = 0.0

    @classmethod
    def create_from_sim(cls, sim: FootSwitchSimulator) -> "FootSwitch":
        """
        ! Class method that creates a FootSwitch instance from a Simulator instance.

        This method uses the components of the Simulator instance to create and return a new FootSwitch instance.
        @param sim  The Simulator instance used to create the FootSwitch.
        @return FootSwitch  The newly created FootSwitch instance.
        """
        return cls(
            FootSwitchCAN(sim.can_node),
            Treadle(sim.hw_board, sim.encoder, sim.motor_dac),
            FswButtons(sim.hw_board),
            Leds(sim.pins, sim.led_driver_adp8866),
            sim.hw_board,
            Batteries(sim.battery1, sim.battery2, sim.adc_driver, sim.pins),
            Position(sim.accelerometer_adxl346),
            sim.async_interface,
        )
