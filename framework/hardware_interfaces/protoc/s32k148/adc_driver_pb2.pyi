import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ADInitParams(_message.Message):
    __slots__ = ("instance_id", "channel_id", "vref_mv", "counts_max", "irq_id")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    VREF_MV_FIELD_NUMBER: _ClassVar[int]
    COUNTS_MAX_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    channel_id: int
    vref_mv: int
    counts_max: int
    irq_id: int
    def __init__(self, instance_id: _Optional[int] = ..., channel_id: _Optional[int] = ..., vref_mv: _Optional[int] = ..., counts_max: _Optional[int] = ..., irq_id: _Optional[int] = ...) -> None: ...

class ADResetParams(_message.Message):
    __slots__ = ("instance_id",)
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    def __init__(self, instance_id: _Optional[int] = ...) -> None: ...

class ADHandle(_message.Message):
    __slots__ = ("instance_id", "channel_id")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    channel_id: int
    def __init__(self, instance_id: _Optional[int] = ..., channel_id: _Optional[int] = ...) -> None: ...

class ADGetValueReturn(_message.Message):
    __slots__ = ("status", "counts")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COUNTS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    counts: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., counts: _Optional[int] = ...) -> None: ...
