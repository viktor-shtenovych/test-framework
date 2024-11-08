from enum import IntEnum
from typing import cast, List

from framework.hardware_interfaces.drivers.s32k148.s32k148_sif_driver import (
    SynchronousIfDevice,
)
from framework.support.reports import logger
from framework.hardware_interfaces.drivers.common.definitions.interfaces import Access


class RawOrientation(IntEnum):
    """
    Raw orientation values.
    """

    kTilted = 0x00
    kX_Positive = 0x03
    kX_Negative = 0x04
    kY_Positive = 0x02
    kY_Negative = 0x05
    kZ_Positive = 0x01
    kZ_Negative = 0x06


class AccelerometerDeviceADXL346(SynchronousIfDevice):
    """
    Accelerometer device ADXL346.
    """

    def __init__(self, instance_id: int, address: int) -> None:
        super().__init__(instance_id, address)

        self.registers = {
            0x00: {"value": [0xE6], "access": Access.R},  # DEVID
            0x1D: {"value": [0x00], "access": Access.RW},  # THRESH_TAP
            0x1E: {"value": [0x00], "access": Access.RW},  # OFSX
            0x1F: {"value": [0x00], "access": Access.RW},  # OFSY
            0x20: {"value": [0x00], "access": Access.RW},  # OFSZ
            0x21: {"value": [0x00], "access": Access.RW},  # DUR
            0x22: {"value": [0x00], "access": Access.RW},  # Latent
            0x23: {"value": [0x00], "access": Access.RW},  # Window
            0x24: {"value": [0x00], "access": Access.RW},  # THRESH_ACT
            0x25: {"value": [0x00], "access": Access.RW},  # THRESH_INACT
            0x26: {"value": [0x00], "access": Access.RW},  # TIME_INACT
            0x27: {"value": [0x00], "access": Access.RW},  # ACT_INACT_CTL
            0x28: {"value": [0x00], "access": Access.RW},  # THRESH_FF
            0x29: {"value": [0x00], "access": Access.RW},  # TIME_FF
            0x2A: {"value": [0x00], "access": Access.RW},  # TAP_AXES
            0x2B: {"value": [0x00], "access": Access.R},  # ACT_TAP_STATUS
            0x2C: {"value": [0x10], "access": Access.RW},  # BW_RATE
            0x2D: {"value": [0x00], "access": Access.RW},  # POWER_CTL
            0x2E: {"value": [0x00], "access": Access.RW},  # INT_ENABLE
            0x2F: {"value": [0x00], "access": Access.RW},  # INT_MAP
            0x30: {"value": [0x00], "access": Access.R},  # INT_SOURCE
            0x31: {"value": [0x00], "access": Access.RW},  # DATA_FORMAT
            0x32: {"value": [0x00], "access": Access.R},  # DATA0
            0x33: {"value": [0x00], "access": Access.R},  # DATA1
            0x34: {"value": [0x00], "access": Access.R},  # DATA2
            0x35: {"value": [0x00], "access": Access.R},  # DATA3
            0x36: {"value": [0x00], "access": Access.R},  # DATA4
            0x37: {"value": [0x00], "access": Access.R},  # DATA5
            0x38: {"value": [0x00], "access": Access.RW},  # FIFO_CTL
            0x39: {"value": [0x00], "access": Access.R},  # FIFO_STATUS
            0x3A: {"value": [0x00], "access": Access.R},  # TAP_SIGN
            0x3B: {"value": [0x01], "access": Access.RW},  # ORIENT_CONF
            0x3C: {"value": [0x4E], "access": Access.R},  # Orient
            # 0xBC: {"value": [0x4E], "access": Access.R},  # orientation (custom register)
        }

    def read(self, size: int) -> bytes:
        """
        Read data from the device.

        Args:
            size: Number of bytes to read.

        Returns:
            bytes: Data read from the device.
        """
        logger.debug(
            f"Accelerometer Read: {size} bytes from register {self._register:02X}"
        )
        if self._register in self.registers:
            data = cast(List[int], self.registers[self._register]["value"])
            if len(data) < size:
                data = data + [0x00] * (size - len(data))
            return bytes(data[:size])
        else:
            # Handle reading from undefined registers by returning zeros
            return bytes([0x00] * size)

    def write(self, data: bytes) -> None:
        """
        Write data to the device.

        Args:
            data: Data to write to the device.
        """
        self._register = data[1] & 0x7F
        if not (data[1] & 0x80):
            logger.debug(
                f"Accelerometer Write: {data.hex()} to register {self._register:02X}"
            )

            if (
                self._register in self.registers
                and self.registers[self._register]["access"] == "R/W"
            ):
                self.registers[self._register]["value"] = list(data[:1])

    def set_orientation(self, value: int) -> None:
        """
        Set orientation.

        Args:
            value: Orientation value.
        """
        self.registers[0x3C]["value"] = [value]
