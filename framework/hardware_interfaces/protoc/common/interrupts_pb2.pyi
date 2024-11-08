import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IdleContext(_message.Message):
    __slots__ = ("idle_cycles",)
    IDLE_CYCLES_FIELD_NUMBER: _ClassVar[int]
    idle_cycles: int
    def __init__(self, idle_cycles: _Optional[int] = ...) -> None: ...

class InterruptContext(_message.Message):
    __slots__ = ("irq_id", "irq_flags", "time")
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    IRQ_FLAGS_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    irq_id: int
    irq_flags: int
    time: int
    def __init__(self, irq_id: _Optional[int] = ..., irq_flags: _Optional[int] = ..., time: _Optional[int] = ...) -> None: ...

class InterruptContextQueue(_message.Message):
    __slots__ = ("queue",)
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    queue: _containers.RepeatedCompositeFieldContainer[InterruptContext]
    def __init__(self, queue: _Optional[_Iterable[_Union[InterruptContext, _Mapping]]] = ...) -> None: ...
