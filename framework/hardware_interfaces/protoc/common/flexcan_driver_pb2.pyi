import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FCIrqFlags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FCIrqFlags_RX_COMPLETE: _ClassVar[FCIrqFlags]
    FCIrqFlags_TX_COMPLETE: _ClassVar[FCIrqFlags]
    FCIrqFlags_ERROR: _ClassVar[FCIrqFlags]

class FCMsgIdType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FCMsgIdType_STD: _ClassVar[FCMsgIdType]
    FCMsgIdType_EXT: _ClassVar[FCMsgIdType]
FCIrqFlags_RX_COMPLETE: FCIrqFlags
FCIrqFlags_TX_COMPLETE: FCIrqFlags
FCIrqFlags_ERROR: FCIrqFlags
FCMsgIdType_STD: FCMsgIdType
FCMsgIdType_EXT: FCMsgIdType

class FCInitParams(_message.Message):
    __slots__ = ("instance_id", "irq_id", "max_num_mb", "num_id_rx_filters")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_NUM_MB_FIELD_NUMBER: _ClassVar[int]
    NUM_ID_RX_FILTERS_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    irq_id: int
    max_num_mb: int
    num_id_rx_filters: int
    def __init__(self, instance_id: _Optional[int] = ..., irq_id: _Optional[int] = ..., max_num_mb: _Optional[int] = ..., num_id_rx_filters: _Optional[int] = ...) -> None: ...

class FCFreezeModeParams(_message.Message):
    __slots__ = ("instance_id",)
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    def __init__(self, instance_id: _Optional[int] = ...) -> None: ...

class FCSendParams(_message.Message):
    __slots__ = ("instance_id", "mb_idx", "msg_id_type", "msg_id", "mb_data")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    MB_IDX_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_TYPE_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    MB_DATA_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    mb_idx: int
    msg_id_type: FCMsgIdType
    msg_id: int
    mb_data: bytes
    def __init__(self, instance_id: _Optional[int] = ..., mb_idx: _Optional[int] = ..., msg_id_type: _Optional[_Union[FCMsgIdType, str]] = ..., msg_id: _Optional[int] = ..., mb_data: _Optional[bytes] = ...) -> None: ...

class FCSetRxIndMaskParams(_message.Message):
    __slots__ = ("instance_id", "mb_idx", "msg_id_type", "mask")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    MB_IDX_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_TYPE_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    mb_idx: int
    msg_id_type: FCMsgIdType
    mask: int
    def __init__(self, instance_id: _Optional[int] = ..., mb_idx: _Optional[int] = ..., msg_id_type: _Optional[_Union[FCMsgIdType, str]] = ..., mask: _Optional[int] = ...) -> None: ...

class FCConfigRxMbParams(_message.Message):
    __slots__ = ("instance_id", "mb_idx", "msg_id_type", "msg_id", "data_length")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    MB_IDX_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_TYPE_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_LENGTH_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    mb_idx: int
    msg_id_type: FCMsgIdType
    msg_id: int
    data_length: int
    def __init__(self, instance_id: _Optional[int] = ..., mb_idx: _Optional[int] = ..., msg_id_type: _Optional[_Union[FCMsgIdType, str]] = ..., msg_id: _Optional[int] = ..., data_length: _Optional[int] = ...) -> None: ...

class FCReceiveReqParams(_message.Message):
    __slots__ = ("instance_id", "mb_idx")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    MB_IDX_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    mb_idx: int
    def __init__(self, instance_id: _Optional[int] = ..., mb_idx: _Optional[int] = ...) -> None: ...

class FCGetReceivedDataParams(_message.Message):
    __slots__ = ("instance_id", "mb_idx")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    MB_IDX_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    mb_idx: int
    def __init__(self, instance_id: _Optional[int] = ..., mb_idx: _Optional[int] = ...) -> None: ...

class FCGetReceivedDataReturn(_message.Message):
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
