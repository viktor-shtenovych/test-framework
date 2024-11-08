"""Simulation of DAC LTC2622.

See - `Footswitch Software Design Description.docx` section 4.3.1.3.7
"""

import copy
from enum import IntEnum
from typing import Callable


from framework.support.reports import logger
from framework.hardware_interfaces.drivers.s32k148.s32k148_sif_driver import (
    SynchronousIfDevice,
)


class Commands(IntEnum):
    """
    Commands.
    """

    WRITE_TO_N = 0x00
    UPDATE_N = 0x01
    WRITE_TO_N_UPDATE_ALL = 0x02
    WRITE_TO_N_UPDATE_N = 0x03
    POWER_DOWN_N = 0x04
    NOP = 0x0F


class Registers(IntEnum):
    """
    Registers.

    DAC_A - DAC A register.
    DAC_B - DAC B register.
    """

    DAC_A = 0x00
    DAC_B = 0x01


REGISTERS_INITIAL_DATA = {Registers.DAC_A: 0, Registers.DAC_B: 0}


class DacLtc2622(SynchronousIfDevice):
    """Simulation of LTC2622."""

    def __init__(self, instance_id: int, address: int, ref_mv: int = 3300) -> None:
        super().__init__(instance_id, address)

        self._ref_mV = ref_mv
        self._MAX_COUNTS = 4095

        self._registers = copy.deepcopy(REGISTERS_INITIAL_DATA)
        self._channel_is_on: list[bool] = [False, False]
        self._on_write_cbs: list[Callable[[bytes], None]] = []

    def read(self, size: int) -> bytes:
        """
        Read data from the device.

        Args:
            size: Number of bytes to read.

        Returns:
            bytes: Data read from the device.
        """
        return bytes([0xFF] * size)

    def write(self, data: bytes) -> None:
        """
        Write data to the device.

        Args:
            data: Data to write to the device.
        """
        logger.debug(f"[LTC2622] Write: {data.hex()}")
        cmd = (data[2] >> 4) & 0x0F
        addr = (data[2]) & 0x0F
        value = (data[1] << 4) | (data[0] >> 4)
        if (
            (Commands(cmd) == Commands.WRITE_TO_N_UPDATE_N)
            or (Commands(cmd) == Commands.WRITE_TO_N_UPDATE_ALL)
            or (Commands(cmd) == Commands.WRITE_TO_N)
        ):
            if addr == 0x0F:
                self._channel_is_on[0] = True
                self._channel_is_on[1] = True
                self._registers[Registers(0)] = value
                self._registers[Registers(1)] = value
            else:
                self._registers[Registers(addr)] = value
                self._channel_is_on[addr] = True
        elif Commands(cmd) == Commands.POWER_DOWN_N:
            if addr == 0x0F:
                self._channel_is_on[0] = False
                self._channel_is_on[1] = False
            else:
                self._channel_is_on[addr] = False

        for cb in self._on_write_cbs:
            cb(data)

    def get_channel_voltage(self, channel: int) -> float:
        """
        Get voltage of the channel.

        Args:
            channel: Channel number.

        Returns:
            float: Voltage of the channel.
        """
        if self.is_channel_on(channel):
            return (
                self._registers[Registers(channel)] * self._ref_mV / 1000.0
            ) / self._MAX_COUNTS
        else:
            return 0

    def subscribe_on_write(self, on_event_cb: Callable[[bytes], None]) -> None:
        """
        Subscribe on write event.

        Args:
            on_event_cb: Callback to call on write event.
        """
        self._on_write_cbs.append(on_event_cb)

    def is_channel_on(self, channel: int) -> bool:
        """
        Check if the channel is on.

        Args:
            channel: Channel number.

        Returns:
            bool: True if the channel is on, False otherwise.
        """
        return self._channel_is_on[channel]
