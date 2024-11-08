import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FtmIcInitParams(_message.Message):
    __slots__ = ("instance", "irq_id", "channel")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    instance: int
    irq_id: int
    channel: int
    def __init__(self, instance: _Optional[int] = ..., irq_id: _Optional[int] = ..., channel: _Optional[int] = ...) -> None: ...

class FtmIcHandle(_message.Message):
    __slots__ = ("instance", "channel")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    instance: int
    channel: int
    def __init__(self, instance: _Optional[int] = ..., channel: _Optional[int] = ...) -> None: ...
