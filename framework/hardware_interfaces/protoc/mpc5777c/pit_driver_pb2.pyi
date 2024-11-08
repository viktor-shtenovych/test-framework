import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PitChannelParams(_message.Message):
    __slots__ = ("instance_id", "channel_id")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    channel_id: int
    def __init__(self, instance_id: _Optional[int] = ..., channel_id: _Optional[int] = ...) -> None: ...

class PitChannelIrqParams(_message.Message):
    __slots__ = ("instance_id", "channel_id", "irq_id")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    channel_id: int
    irq_id: int
    def __init__(self, instance_id: _Optional[int] = ..., channel_id: _Optional[int] = ..., irq_id: _Optional[int] = ...) -> None: ...

class PitSetPeriodByUsParams(_message.Message):
    __slots__ = ("instance_id", "channel_id", "period_us")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PERIOD_US_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    channel_id: int
    period_us: int
    def __init__(self, instance_id: _Optional[int] = ..., channel_id: _Optional[int] = ..., period_us: _Optional[int] = ...) -> None: ...
