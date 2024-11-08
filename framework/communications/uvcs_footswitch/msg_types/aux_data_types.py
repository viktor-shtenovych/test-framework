import dataclasses
import struct
from enum import IntEnum
from typing import TypeAlias
import bitstruct


class AuxDataType(IntEnum):
    """
    Aux Data Type.

    The Aux Data Type (Byte 11) is incremented on each packet transmission.
    See more in Console Software Communication Specification - Footswitch 4.1.1
    """

    ErrorFlags = 0
    FootSwitchId = 1
    FootSwitchSwVersion = 2
    BatteryStatus1 = 3
    ErrorFlags1 = 4
    RxWirelessSignalStrength = 5
    FootSwitchHwRevision = 6
    ModemFirmwareVersion = 7
    ErrorFlags2 = 8
    Battery1LotNumber = 9
    RawTreadleStatus = 10
    BatteryStatus2 = 11
    ErrorFlags3 = 12
    SerialNumber1 = 13
    SerialNumber2 = 14
    SerialNumber3 = 15
    ErrorFlags4 = 16
    BatteryStatus3 = 17
    BatteryStatus4 = 18
    BatteryStatus5 = 19
    ErrorFlags5 = 20
    Debug = 21
    AccelerometerStatus = 22
    Battery1Version = 23
    ErrorFlags6 = 24
    Battery2LotNumber = 25
    Battery2Version = 26
    BatteryDebugInfo = 27
    ErrorFlags7 = 28
    Reserved = 29
    Reserved1 = 30
    CompatibilityInfo = 31


class OrientationStatus(IntEnum):
    """
    Footswitch Orientation.
    """

    Tilted = 0
    FacingUp = 1
    FacingDown = 2
    VerticalUp = 3
    VerticalDown = 4
    SidewaysRight = 5
    SidewaysLeft = 6


@dataclasses.dataclass
class FootSwitchId:
    """
    A class representing the FootSwitch ID.
    """

    footswitch_id: int

    @classmethod
    def unpack(cls, data: bytes) -> "FootSwitchId":
        """
        Method returning FootSwitch id from data bytes.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            footswitch_id (FootSwitchId): FootSwitch ID
        """
        footswitch_id = int.from_bytes(data[4:6], "little")
        return FootSwitchId(footswitch_id=footswitch_id)


@dataclasses.dataclass
class FootSwitchSwVersion:
    """
    A class representing the FootSwitch softweare version.
    """

    major_version: int
    minor_version: int
    development_version: int

    @classmethod
    def unpack(cls, data: bytes) -> "FootSwitchSwVersion":
        """
        Method returning FootSwitch softweare version from data bytes.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            major_version (FootSwitchSwVersion): Footswitch Software Major Version
            minor_version (FootSwitchSwVersion): Footswitch Software Minor Version
            development_version (FootSwitchSwVersion): Footswitch Software Development Version
        """
        if len(data) < 3:
            raise ValueError("Data is too short to unpack FootSwitchSwVersion")
        major_version, minor_version, development_version = bitstruct.unpack(
            "u4u8u8", data[:3]
        )
        return cls(
            major_version=major_version,
            minor_version=minor_version,
            development_version=development_version,
        )


@dataclasses.dataclass
class ErrorFlags:
    """
    A class representing the FootSwitch Error Flags.
    """

    battery_comm_error: bool
    battery_failure: bool
    modem_failure: bool
    can_comm_timeout: bool
    recovered_from_crit_error: bool
    recovered_from_comm_error: bool
    pairing_data_corrupt: bool
    wireless_operation_failure: bool
    up_switch_failure: bool
    left_vertical_switch_failure: bool
    left_horizontal_switch_failure: bool
    right_vertical_switch_failure: bool
    right_horizontal_switch_failure: bool
    treadle_excessive_travel: bool
    detent_motor_failure: bool
    treadle_homing_failure: bool
    right_heel_switch_failure: bool
    left_heel_switch_failure: bool
    laser_footswitch_right_switch_failure: bool
    laser_footswitch_center_switch_failure: bool
    laser_footswitch_left_switch_failure: bool

    @classmethod
    def unpack(cls, data: bytes) -> "ErrorFlags":
        """
        Method returning FootSwitch Error Flag from data bytes.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            byte_4 (ErrorFlags): Battery Communication Error
            byte_5 (ErrorFlags): Battery Failure
            byte_6 (ErrorFlags): Modem Failure
        """
        byte_4 = list(bitstruct.unpack("b1b1b1b1b1b1b1b1", data[0:1]))
        byte_5 = list(bitstruct.unpack("b1b1b1b1b1b1b1b1", data[1:2]))
        byte_6 = list(bitstruct.unpack("p3b1b1b1b1b1", data[2:3]))

        # reverse lists as bit 0 as the last one
        byte_4.reverse()
        byte_5.reverse()
        byte_6.reverse()

        all_values = byte_4 + byte_5 + byte_6

        return ErrorFlags(*all_values)


@dataclasses.dataclass
class RxWirelessSignalStrength:
    """
    A class representing the Rx Wireless Signal Strength.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "RxWirelessSignalStrength":
        """
        Method returning the Rx Wireless Signal Strength.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            RxWirelessSignalStrength
        """
        # TODO: Implement
        return RxWirelessSignalStrength()


@dataclasses.dataclass
class FootSwitchHwRevision:
    """
    A class representing the FootSwitch Hardware Revision.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "FootSwitchHwRevision":
        """
        Method returning the FootSwitch Hardware Revision.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            FootSwitchHwRevision
        """
        # TODO: Implement
        return FootSwitchHwRevision()


@dataclasses.dataclass
class ModemFirmwareVersion:
    """
    A class representing the Modem Firmware Version.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "ModemFirmwareVersion":
        """
        Method returning the Modem Firmware Version.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            ModemFirmwareVersion
        """
        # TODO: Implement
        return ModemFirmwareVersion()


@dataclasses.dataclass
class Battery1LotNumber:
    """
    A class representing the FootSwitch Battery 1 Lot Number.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "Battery1LotNumber":
        """
        Method returning the FootSwitch Battery 1 Lot Number.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            Battery1LotNumber
        """
        # TODO: Implement
        return Battery1LotNumber()


@dataclasses.dataclass
class RawTreadleStatus:
    """
    A class representing the FootSwitch Raw Treadle Status.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "RawTreadleStatus":
        """
        Method returning the FootSwitch Raw Treadle Status.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            RawTreadleStatus
        """
        # TODO: Implement
        return RawTreadleStatus()


@dataclasses.dataclass
class BatteryStatus2:
    """
    A class representing the FootSwitch Battery Status 2.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "BatteryStatus2":
        """
        Method returning the FootSwitch Battery Status 2.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            BatteryStatus2
        """
        # TODO: Implement
        return BatteryStatus2()


@dataclasses.dataclass
class SerialNumber1:
    """
    A class representing the FootSwitch Serial Number 1.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "SerialNumber1":
        """
        Method returning the FootSwitch Serial Number 1.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            SerialNumber1
        """
        # TODO: Implement
        return SerialNumber1()


@dataclasses.dataclass
class SerialNumber2:
    """
    A class representing the FootSwitch Serial Number 2.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "SerialNumber2":
        """
        Method returning the FootSwitch Serial Number 2.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            SerialNumber2
        """
        # TODO: Implement
        return SerialNumber2()


@dataclasses.dataclass
class SerialNumber3:
    """
    A class representing the FootSwitch Serial Number 3.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "SerialNumber3":
        """
        Method returning the FootSwitch Serial Number 3.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            SerialNumber3
        """
        # TODO: Implement
        return SerialNumber3()


@dataclasses.dataclass
class BatteryStatus3:
    """
    A class representing the FootSwitch Battery Status 3.
    """

    voltage: int
    average_current: int

    @classmethod
    def unpack(cls, data: bytes) -> "BatteryStatus3":
        """
        Method returning the FootSwitch Battery Status 3.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            BatteryStatus3
        """
        return BatteryStatus3(*struct.unpack(">Hh", data))


@dataclasses.dataclass
class BatteryStatus4:
    """
    A class representing the FootSwitch Battery Status 4.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "BatteryStatus4":
        """
        Method returning the FootSwitch Battery Status 4.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            BatteryStatus4
        """
        # TODO: Implement
        return BatteryStatus4()


@dataclasses.dataclass
class BatteryStatus5:
    """
    A class representing the FootSwitch Battery Status 5.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "BatteryStatus5":
        """
        Method returning the FootSwitch Battery Status 5.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            BatteryStatus5
        """
        # TODO: Implement
        return BatteryStatus5()


@dataclasses.dataclass
class Debug:
    """
    A class to debugging.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "Debug":
        """
        Method returning the debugging data.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            Debug
        """
        # TODO: Implement
        return Debug()


@dataclasses.dataclass
class AccelerometerStatus:
    """
    A class representing the Accellerometr Status of FootSwitch.
    """

    footswitch_orientation: OrientationStatus

    @classmethod
    def unpack(cls, data: bytes) -> "AccelerometerStatus":
        """
        Method returning the Accellerometr Status of FootSwitch.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            footswitch_orientation (OrientationStatus): AccelerometerStatus
        """
        orietation = int.from_bytes(data, "little")
        return AccelerometerStatus(footswitch_orientation=OrientationStatus(orietation))


@dataclasses.dataclass
class Battery1Version:
    """
    A class representing the FootSwitch Battery 1 Version.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "Battery1Version":
        """
        Method returning the FootSwitch Battery 1 Version.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            Battery1Version
        """
        # TODO: Implement
        return Battery1Version()


@dataclasses.dataclass
class Battery2LotNumber:
    """
    A class representing the FootSwitch Battery 2 Lot Number.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "Battery2LotNumber":
        """
        Method returning the FootSwitch Battery 2 Lot Number.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            Battery2LotNumber
        """
        # TODO: Implement
        return Battery2LotNumber()


@dataclasses.dataclass
class Battery2Version:
    """
    A class representing the FootSwitch Battery 2 Version.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "Battery2Version":
        """
        Method returning the FootSwitch Battery 2 Version.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            Battery2Version
        """
        # TODO: Implement
        return Battery2Version()


@dataclasses.dataclass
class BatteryDebugInfo:
    """
    A class representing the FootSwitch Battery Debug Info.
    """

    battery1_soc: int
    battery1_soh: int
    battery2_soc: int
    battery2_soh: int

    @classmethod
    def unpack(cls, data: bytes) -> "BatteryDebugInfo":
        """
        Method returning the FootSwitch Battery Debug Info.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            BatteryDebugInfo
        """
        return BatteryDebugInfo(*struct.unpack("BBBB", data))


@dataclasses.dataclass
class Reserved:
    """
    A class representing the Reserved data.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "Reserved":
        """
        Method returning the Reserved data.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            Reserved
        """
        # TODO: Implement
        return Reserved()


@dataclasses.dataclass
class Reserved1:
    """
    A class representing the Reserved 1 data.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "Reserved1":
        """
        Method returning the Reserved 1 data.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            Reserved1
        """
        # TODO: Implement
        return Reserved1()


@dataclasses.dataclass
class CompatibilityInfo:
    """
    A class representing the Compatibility Info.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "CompatibilityInfo":
        """
        Method returning the Compatibility Info.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            CompatibilityInfo
        """
        # TODO: Implement
        return CompatibilityInfo()


@dataclasses.dataclass
class BatteryStatus1:
    """
    A class representing the Battery Status 1.
    """

    level: int
    charging: bool
    status_unknown: bool
    battery_low: bool
    battery_crit_low: bool
    battery_depleted: bool
    soh_status_unknown: bool
    battery_over_temperature: bool
    battery_temperature: int
    battery_soh: int

    @classmethod
    def unpack(cls, data: bytes) -> "BatteryStatus1":
        """
        Method returning the the Battery Status 1.

        Args:
            data (bytes): raw data packet from can communications

        Returns:
            level (Bool): Battery Battery Level
            charging (Unsigned): Charging
            status_unknown (Bool): Status Unknown
            battery_low (Bool): Battery Low
            battery_crit_low (Bool): Battery Critically Low
            battery_depleted (Bool): Battery Depleted
            soh_status_unknown (Bool): SoH Status Unknown
            battery_over_temperature (Bool): Battery Over Temperature
            battery_temperature (Signed): Battery Temperature
            battery_soh (Unsigned): Battery SoH
        """
        (
            charging,
            level,
            status_unknown,
            battery_low,
            battery_crit_low,
            battery_depleted,
            soh_status_unknown,
            battery_over_temperature,
            _,
            _,
            battery_temperature,
            battery_soh,
        ) = bitstruct.unpack("b1u7b1b1b1b1b1b1b1b1u8u8", data)

        return BatteryStatus1(
            level=level,
            charging=charging,
            status_unknown=status_unknown,
            battery_low=battery_low,
            battery_crit_low=battery_crit_low,
            battery_depleted=battery_depleted,
            soh_status_unknown=soh_status_unknown,
            battery_over_temperature=battery_over_temperature,
            battery_temperature=battery_temperature,
            battery_soh=battery_soh,
        )


AuxDataFlags = tuple(
    flag for flag in AuxDataType if not flag.name.startswith("ErrorFlags")
)
AuxDataErrorFlags = tuple(
    flag for flag in AuxDataType if flag.name.startswith("ErrorFlags")
)

_aux_data_classes = {
    ErrorFlags,
    FootSwitchId,
    FootSwitchSwVersion,
    BatteryStatus1,
    RxWirelessSignalStrength,
    FootSwitchHwRevision,
    ModemFirmwareVersion,
    Battery1LotNumber,
    RawTreadleStatus,
    BatteryStatus2,
    SerialNumber1,
    SerialNumber2,
    SerialNumber3,
    BatteryStatus3,
    BatteryStatus4,
    BatteryStatus5,
    Debug,
    AccelerometerStatus,
    Battery1Version,
    Battery2LotNumber,
    Battery2Version,
    BatteryDebugInfo,
    Reserved,
    Reserved1,
    CompatibilityInfo,
}

AuxData: TypeAlias = (
    ErrorFlags
    | FootSwitchId
    | FootSwitchSwVersion
    | BatteryStatus1
    | RxWirelessSignalStrength
    | FootSwitchHwRevision
    | ModemFirmwareVersion
    | Battery1LotNumber
    | RawTreadleStatus
    | BatteryStatus2
    | SerialNumber1
    | SerialNumber2
    | SerialNumber3
    | BatteryStatus3
    | BatteryStatus4
    | BatteryStatus5
    | Debug
    | AccelerometerStatus
    | Battery1Version
    | Battery2LotNumber
    | Battery2Version
    | BatteryDebugInfo
    | Reserved
    | Reserved1
    | CompatibilityInfo
)

aux_data_classes = {cls.__name__: cls for cls in _aux_data_classes}
