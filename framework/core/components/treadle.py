from collections import deque
from enum import Enum
from typing import Deque

from framework.core.control.encoder import Encoder
from framework.core.boards.fsw.hw_board import HwBoard
from framework.core.devices.dac_ltc2622 import DacLtc2622
from framework.support.vtime.virtual_time import vtime_manager

from framework.support.reports import logger


class TreadleState(Enum):
    """
    Treadle state.
    """

    UP = True
    DOWN = False


class Treadle:
    """Simulation of treadle component. See 'Footswitch Software Design Description.docx' section 4.3.1.2.1 Treadle."""

    def __init__(self, board: HwBoard, encoder: Encoder, motor_dac: DacLtc2622) -> None:
        self._switches = [
            board.up_switch_0,
            board.up_switch_1,
            board.up_switch_2,
            board.up_switch_3,
            board.up_switch_4,
        ]
        self.encoder = encoder
        self._TREADLE_MAX_COUNTS = 4095
        self._TREADLE_MIN_COUNTS = 0
        self._TREADLE_UP_ENC_COUNTS = (
            1000  # Anterior Footswitch Encoder (Footswitch SDD) Line A
        )
        self._TREADLE_FULL_RANGE_ENC_COUNTS = (
            1431  # Anterior Footswitch Encoder (Footswitch SDD) 10 degrees
        )

        self.detent_temp = board.detent_temp
        self.detent_temp.voltage = (
            25 * (-0.01169) + 1.8663
        )  # 25 C, formula from the LM20 datasheet

        self.detent_current = board.detent_current
        self.detent_current.voltage = 0

        self._is_detent_occurred = False
        self._detent_timestamps: Deque[float] = deque(maxlen=5)

        self.detent_en = board.detent_en

        self.motor_dac = motor_dac

        def detent_en_state_change_handler(state: bool) -> None:
            """
            Handle detent_en state change.

            Args:
                state: State of detent_en.
            """
            if state:
                self.detent_current.voltage = self.motor_dac.get_channel_voltage(0)
            else:
                self.handle_detent_en_false()

        def dac_on_write_cb(data: bytes) -> None:
            """
            Handle DAC on write.

            Args:
                data: Data to write.
            """
            if self.detent_en.state:
                self.detent_current.voltage = self.motor_dac.get_channel_voltage(0)
                self._update_detent_status()
            else:
                self.detent_current.voltage = 0

        self.motor_dac.subscribe_on_write(dac_on_write_cb)
        self.detent_en.subscribe_on_state_change(detent_en_state_change_handler)

    def _update_detent_status(self) -> None:
        """
        Update detent status.

        The detent status is updated based on the current voltage of the detent current sensor.
        """
        current_time = vtime_manager.time_ms()
        if self.detent_current.voltage >= 0.49:
            self._detent_timestamps.append(current_time)
            #  A detent bump consists of 5 pulses, each pulse has an on time of 10ms
            #  and an off time of 20ms for a total of 130ms.
            if (
                len(self._detent_timestamps) >= 5
                and (current_time - self._detent_timestamps[0]) <= 130
            ):
                self._is_detent_occurred = True
                logger.debug(f"Detent timestamps: {self._detent_timestamps}")

    def _set_switches(self, strength: int, value: bool) -> None:
        """
        Set switches.

        Args:
            strength: Strength of the switches.
            value: Value to set.
        """
        if strength > 5 or strength < 0:
            raise AttributeError("Strength shall be in range 0-5")

        for switch in self._switches[: strength + 1]:
            switch.state = value
        for switch in self._switches[strength:]:
            switch.state = not value

    def up(self, strength: int = 5) -> None:
        """
        Move treadle up.

        Args:
            strength: Strength of the treadle.
        """
        self._set_switches(strength, True)
        self.encoder.set_value(int(self._TREADLE_UP_ENC_COUNTS))

    def down(self, treadle_counter: int, strength: int = 5) -> None:
        """
        Move treadle down.

        Args:
            treadle_counter: Treadle counter.
            strength: Strength of the treadle.
        """
        self._set_switches(strength, False)
        ratio = treadle_counter / (self._TREADLE_MAX_COUNTS - self._TREADLE_MIN_COUNTS)
        self.encoder.set_value(
            int(
                self._TREADLE_UP_ENC_COUNTS
                + ratio * self._TREADLE_FULL_RANGE_ENC_COUNTS
            )
        )

    def status(self) -> TreadleState:
        """
        Get treadle status.
        """
        return (
            TreadleState.UP
            if len([switch.state for switch in self._switches]) >= 3
            else TreadleState.DOWN
        )

    def is_detent_occurred(self) -> bool:
        """
        Check if detent occurred.
        """
        return self._is_detent_occurred

    def clear_detent_detection(self) -> None:
        """
        Clear detent detection.
        """
        self._is_detent_occurred = False
        self._detent_timestamps.clear()

    def handle_detent_en_false(self) -> None:
        """
        Handle detent_en false.
        """
        self.detent_current.voltage = 0
        self.clear_detent_detection()
