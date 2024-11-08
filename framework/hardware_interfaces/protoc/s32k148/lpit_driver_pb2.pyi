import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LpitInitParams(_message.Message):
    __slots__ = ("timer_id", "irq_id")
    TIMER_ID_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    timer_id: int
    irq_id: int
    def __init__(self, timer_id: _Optional[int] = ..., irq_id: _Optional[int] = ...) -> None: ...

class LpitHandle(_message.Message):
    __slots__ = ("timer_id",)
    TIMER_ID_FIELD_NUMBER: _ClassVar[int]
    timer_id: int
    def __init__(self, timer_id: _Optional[int] = ...) -> None: ...

class LpitSetPeriodParams(_message.Message):
    __slots__ = ("timer_id", "period")
    TIMER_ID_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    timer_id: int
    period: int
    def __init__(self, timer_id: _Optional[int] = ..., period: _Optional[int] = ...) -> None: ...
