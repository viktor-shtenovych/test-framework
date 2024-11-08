"""Simulation of BQ40Z50.

https://www.ti.com/lit/ug/sluubc1d/sluubc1d.pdf?ts=1716369611432&ref_url=https%253A%252F%252Fwww.google.com%252F
See - `Footswitch Software Design Description.docx` section 4.3.1.2.5
"""

import copy
import struct
from enum import IntEnum


from framework.support.reports import logger
from framework.hardware_interfaces.drivers.s32k148.s32k148_sif_driver import (
    SynchronousIfDevice,
)


class ManufacturerAccess(IntEnum):
    """
    Manufacturer access registers.
    """

    ManufacturerAccess = 0x0000
    DeviceType = 0x0001
    FirmwareVersion = 0x0002
    HardwareVersion = 0x0003
    ChemicalId = 0x0006
    SafetyStatus = 0x00051
    PFStatus = 0x0053


class Registers(IntEnum):
    """
    BQ40z50 registers.
    """

    Temperature = 0x08
    Voltage = 0x09
    Current = 0x0A
    AverageCurrent = 0x0B
    MaxError = 0x0C
    RelativeStateOfCharge = 0x0D
    AbsoluteStateOfCharge = 0x0E
    RemainingCapacity = 0x0F
    FullChargeCapacity = 0x10
    RuntimeToEmpty = 0x11
    AverageTimeToEmpty = 0x12
    AverageTimeToFull = 0x13
    ChargingCurrent = 0x14
    ChargingVoltage = 0x15
    BatteryStatus = 0x16
    CycleCount = 0x17
    DesignCapacity = 0x18
    ManufacturerDate = 0x1B
    SerialNumber = 0x1C
    ManufacturerData = 0x23
    StateOfHealth = 0x4F


REGISTERS_INITIAL_DATA = {
    Registers.Temperature: struct.pack(
        "<H", (273 + 30) * 10
    ),  # 10 deg C in 0.1 Kelvins,
    Registers.Voltage: struct.pack("<H", int(8.5 * 1e3)),  # 5300 mV
    Registers.AverageCurrent: struct.pack("<H", 100),  # 100 mA
    Registers.RelativeStateOfCharge: bytes([35, 00]),  # 35 %
    Registers.ManufacturerDate: bytes([0xB6, 0x58]),  # 22.5.2024
    Registers.SerialNumber: bytes([0xA5, 0x0F]),
    Registers.MaxError: bytes([0, 60]),
    Registers.DesignCapacity: bytes([0x30, 0x11]),
    Registers.AbsoluteStateOfCharge: struct.pack("<H", 95),  # 95 %
    Registers.RemainingCapacity: struct.pack("<H", 500),
    Registers.FullChargeCapacity: struct.pack("<H", 2500),
    Registers.AverageTimeToEmpty: struct.pack("<H", 30),
    Registers.AverageTimeToFull: struct.pack("<H", 65530),
    Registers.ChargingCurrent: struct.pack("<h", 0),
    Registers.ChargingVoltage: struct.pack("<h", 0),
    Registers.BatteryStatus: bytes([0x00, 0x00]),
    Registers.CycleCount: struct.pack("<H", 50),
    Registers.StateOfHealth: bytes([100, 0]),
}

MANUFACTURER_INITIAL_DATA = {
    ManufacturerAccess.DeviceType: bytes([0x01, 0x02]),
    ManufacturerAccess.FirmwareVersion: bytes(
        [0xFF, 0xAA, 0x01, 0x01, 0x0F, 0x00, 0xAA, 0x00, 0x00, 0x00, 0x00]
    ),
    ManufacturerAccess.HardwareVersion: bytes([0x06, 0x05]),
    ManufacturerAccess.ChemicalId: bytes([0x08, 0x07]),
    ManufacturerAccess.SafetyStatus: bytes([0x00, 0x00, 0x00, 0x00]),
    ManufacturerAccess.PFStatus: bytes([0x00, 0x00, 0x00, 0x00]),
}


class BatteryPackManagerBq40z50(SynchronousIfDevice):
    """Simulation of BQ40z50."""

    def __init__(self, instance_id: int, address: int) -> None:
        super().__init__(instance_id, address)
        self._selected_register: int = 0
        self._manufacturer_data_register: int = 0

        self._registers = copy.deepcopy(REGISTERS_INITIAL_DATA)
        self._manufacturer_data_registers = copy.deepcopy(MANUFACTURER_INITIAL_DATA)
        self._connected = True

    def connect(self) -> None:
        """
        Connects the battery.
        """
        self._connected = True

    def disconnect(self) -> None:
        """
        Disconnects the battery.
        """
        self._connected = False

    def set_charge_level(self, value: int) -> None:
        """
        Sets the charge level.
        """
        self._registers[Registers.RelativeStateOfCharge] = struct.pack("<H", value)

    def set_average_current(self, value: int) -> None:
        """
        Sets the average current.
        """
        self._registers[Registers.AverageCurrent] = struct.pack("<h", value)

    def set_state_of_health(self, value: int) -> None:
        """
        Sets the state of health.
        """
        self._registers[Registers.StateOfHealth] = struct.pack("<h", value)

    def read(self, size: int) -> bytes:
        """
        Reads the data from the battery.
        """
        if not self._connected:
            raise TimeoutError("Battery is disconnected")

        if self._selected_register == Registers.ManufacturerData:
            logger.debug(
                f"[BQ40z50] Reading manufacturer data for {self._manufacturer_data_register}, size({size})"
            )
            data = self._manufacturer_data_registers[
                ManufacturerAccess(self._manufacturer_data_register)
            ]
            return bytes([size - 1]) + data[: size - 1]
        else:
            logger.debug(f"[BQ40z50] Reading register: {self._selected_register}")
            return self._registers[Registers(self._selected_register)]

    def write(self, data: bytes) -> None:
        """
        Writes the data to the battery.
        """
        if not self._connected:
            raise TimeoutError("Battery is disconnected")

        logger.debug(f"[BQ40z50] Write: {data.hex()}")
        if len(data) == 3:
            self._manufacturer_data_register = struct.unpack("<H", data[1:])[0]
        else:
            self._selected_register = data[0]
