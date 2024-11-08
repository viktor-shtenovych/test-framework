import dataclasses
import struct

from typing import Optional, cast

from framework.communications.uvcs_footswitch.msg_types.aux_data_types import (
    AuxDataType,
    AuxDataErrorFlags,
    ErrorFlags,
    AuxData,
    AuxDataFlags,
    aux_data_classes,
)
from framework.communications.uvcs_footswitch.msg_types.msg_data_structures import (
    FootSwitchType,
    FootSwitchState,
    Buttons,
    LaserButtons,
)
from framework.support.reports import logger


@dataclasses.dataclass
class StatusMsg210:
    foot_switch_type: FootSwitchType
    foot_switch_state: FootSwitchState
    tx_counter: int
    buttons: Buttons
    treadle_count: int
    laser_buttons: LaserButtons

    @classmethod
    def unpack(cls, data: bytes) -> "StatusMsg210":
        (
            foot_switch_type_int,
            foot_switch_state_int,
            tx_counter,
            buttons,
            count,
            buttons2,
            _,
        ) = struct.unpack(">BBBcHcB", data)

        return StatusMsg210(
            foot_switch_type=FootSwitchType(foot_switch_type_int),
            foot_switch_state=FootSwitchState(foot_switch_state_int),
            tx_counter=tx_counter,
            buttons=Buttons.unpack(buttons),
            treadle_count=count,
            laser_buttons=LaserButtons.unpack(buttons2),
        )


@dataclasses.dataclass
class StatusMsg211:
    aux_type: AuxDataType
    data: Optional[AuxData]

    @classmethod
    def unpack(cls, data: bytes) -> "StatusMsg211":
        aux_type = AuxDataType(data[3])
        aux_data: Optional[AuxData] = None
        match aux_type:
            case flag if flag in AuxDataErrorFlags:
                aux_data = ErrorFlags.unpack(data[4:])
            case flag if flag in AuxDataFlags:
                dtype = cast(AuxData, aux_data_classes[flag.name])
                aux_data = dtype.unpack(data[4:])
            case _:
                logger.error(f"Unknown AuxType: {data[3]}")
        return StatusMsg211(aux_type, aux_data)


@dataclasses.dataclass
class StatusMsg212:
    newest_supported_proto_version: int
    oldest_supported_proto_version: int
    foot_switch_type: FootSwitchType
    session_id: int

    @classmethod
    def unpack(cls, data: bytes) -> "StatusMsg212":
        (
            newest_supported_proto_version,
            oldest_supported_proto_version,
            foot_switch_type_int,
            session_id,
            _,
            _,
            _,
        ) = struct.unpack("<BBBHBBB", data)

        return StatusMsg212(
            newest_supported_proto_version=newest_supported_proto_version,
            oldest_supported_proto_version=oldest_supported_proto_version,
            foot_switch_type=FootSwitchType(foot_switch_type_int),
            session_id=session_id,
        )
