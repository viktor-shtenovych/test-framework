import dataclasses
from enum import IntEnum

import bitstruct

from framework.communications.uvcs_footswitch.msg_types.msg_data_structures import (
    FootSwitchType,
)


class FootSwitchPowerState(IntEnum):
    """
    Foot switch power state.
    """

    Cabled = 0
    Cradled = 1
    Active = 2
    Standby = 3
    Sleep = 4
    Fault = 5


class FaultType(IntEnum):
    """
    Fault type.
    """

    NoNe = 0
    EncoderFailure = 1
    BrokenSpring = 2
    AccelerometerFailure = 3
    WatchdogTimeout = 4
    SoftwareError = 5
    BatteryCommFailure = 6
    BatteryFailure = 7
    WirelessDataOutOfRange = 8
    CANDataOutOfRange = 9


@dataclasses.dataclass
class Fault010:
    """
    Fault 010.
    """

    foot_switch_type: FootSwitchType
    format_version: int
    foot_switch_power_state: FootSwitchPowerState
    file_id: int
    fault_type: FaultType
    file_line_no: int
    foot_switch_id: int

    @classmethod
    def unpack(cls, data: bytes) -> "Fault010":
        """
        Unpack data.

        Args:
            data: Data to unpack.

        Returns:
            Fault010: Unpacked data.
        """
        (
            format_version,
            foot_switch_type_int,
            reserved,
            foot_switch_power_state_int,
            file_id,
            fault_type,
            file_line_no,
            foot_switch_id,
        ) = tuple(bitstruct.unpack("u5u3u4u4u8u8u16u16", data))
        return Fault010(
            foot_switch_type=FootSwitchType(foot_switch_type_int),
            format_version=format_version,
            foot_switch_power_state=FootSwitchPowerState(foot_switch_power_state_int),
            file_id=file_id,
            fault_type=FaultType(fault_type),
            file_line_no=file_line_no,
            foot_switch_id=foot_switch_id,
        )


@dataclasses.dataclass
class Fault011:
    """
    Fault 011.
    """

    foot_switch_software_major_version: int
    foot_switch_software_minor_version: int
    foot_switch_software_dev_version: int
    fault_detail: int

    @classmethod
    def unpack(cls, data: bytes) -> "Fault011":
        """
        Unpack data.

        Args:
            data: Data to unpack.

        Returns:
            Fault011: Unpacked data.
        """
        (
            foot_switch_software_major_version,
            reserved,
            foot_switch_software_minor_version,
            foot_switch_software_dev_version,
            fault_detail,
        ) = tuple(bitstruct.unpack("u4u4u8u8u16", data))
        return Fault011(
            foot_switch_software_major_version=foot_switch_software_major_version,
            foot_switch_software_minor_version=foot_switch_software_minor_version,
            foot_switch_software_dev_version=foot_switch_software_dev_version,
            fault_detail=fault_detail,
        )
