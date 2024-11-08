import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MCIrqFlags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MCIrqFlags_RX_COMPLETE: _ClassVar[MCIrqFlags]
    MCIrqFlags_TX_COMPLETE: _ClassVar[MCIrqFlags]
    MCIrqFlags_RX0FIFO_COMPLETE: _ClassVar[MCIrqFlags]

class MCMsgIdType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MCMsgIdType_STD: _ClassVar[MCMsgIdType]
    MCMsgIdType_EXT: _ClassVar[MCMsgIdType]

class MCMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MC_NORMAL_MODE: _ClassVar[MCMode]
    MC_LISTEN_ONLY_MODE: _ClassVar[MCMode]
    MC_LOOPBACK_MODE: _ClassVar[MCMode]
    MC_TEST_MODE: _ClassVar[MCMode]
    MC_DISABLE_MODE: _ClassVar[MCMode]
MCIrqFlags_RX_COMPLETE: MCIrqFlags
MCIrqFlags_TX_COMPLETE: MCIrqFlags
MCIrqFlags_RX0FIFO_COMPLETE: MCIrqFlags
MCMsgIdType_STD: MCMsgIdType
MCMsgIdType_EXT: MCMsgIdType
MC_NORMAL_MODE: MCMode
MC_LISTEN_ONLY_MODE: MCMode
MC_LOOPBACK_MODE: MCMode
MC_TEST_MODE: MCMode
MC_DISABLE_MODE: MCMode

class MCInitParams(_message.Message):
    __slots__ = ("instance_id", "mode", "fd_enable", "payload", "irq_id", "max_num_mb", "num_id_rx_filters")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    FD_ENABLE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_NUM_MB_FIELD_NUMBER: _ClassVar[int]
    NUM_ID_RX_FILTERS_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    mode: MCMode
    fd_enable: int
    payload: int
    irq_id: int
    max_num_mb: int
    num_id_rx_filters: int
    def __init__(self, instance_id: _Optional[int] = ..., mode: _Optional[_Union[MCMode, str]] = ..., fd_enable: _Optional[int] = ..., payload: _Optional[int] = ..., irq_id: _Optional[int] = ..., max_num_mb: _Optional[int] = ..., num_id_rx_filters: _Optional[int] = ...) -> None: ...

class MCSendParams(_message.Message):
    __slots__ = ("instance_id", "vmb_idx", "msg_id_type", "msg_id", "mb_data")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    VMB_IDX_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_TYPE_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    MB_DATA_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    vmb_idx: int
    msg_id_type: MCMsgIdType
    msg_id: int
    mb_data: bytes
    def __init__(self, instance_id: _Optional[int] = ..., vmb_idx: _Optional[int] = ..., msg_id_type: _Optional[_Union[MCMsgIdType, str]] = ..., msg_id: _Optional[int] = ..., mb_data: _Optional[bytes] = ...) -> None: ...

class MCSetRxFifoFiletrMaskParams(_message.Message):
    __slots__ = ("instance_id", "msg_id_type", "fl_idx", "id", "mask")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_TYPE_FIELD_NUMBER: _ClassVar[int]
    FL_IDX_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    msg_id_type: MCMsgIdType
    fl_idx: int
    id: int
    mask: int
    def __init__(self, instance_id: _Optional[int] = ..., msg_id_type: _Optional[_Union[MCMsgIdType, str]] = ..., fl_idx: _Optional[int] = ..., id: _Optional[int] = ..., mask: _Optional[int] = ...) -> None: ...

class MCReceiveReqParams(_message.Message):
    __slots__ = ("instance_id", "vmb_idx")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    VMB_IDX_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    vmb_idx: int
    def __init__(self, instance_id: _Optional[int] = ..., vmb_idx: _Optional[int] = ...) -> None: ...

class MCGetReceivedDataParams(_message.Message):
    __slots__ = ("instance_id", "vmb_idx")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    VMB_IDX_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    vmb_idx: int
    def __init__(self, instance_id: _Optional[int] = ..., vmb_idx: _Optional[int] = ...) -> None: ...

class MCGetReceivedDataReturn(_message.Message):
    __slots__ = ("status", "instance_id", "msg_id", "mb_data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    MB_DATA_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    instance_id: int
    msg_id: int
    mb_data: bytes
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., instance_id: _Optional[int] = ..., msg_id: _Optional[int] = ..., mb_data: _Optional[bytes] = ...) -> None: ...
