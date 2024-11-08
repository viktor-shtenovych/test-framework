import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RtcHandle(_message.Message):
    __slots__ = ("instance",)
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    instance: int
    def __init__(self, instance: _Optional[int] = ...) -> None: ...

class RtcInitParams(_message.Message):
    __slots__ = ("instance", "seconds_irq_id", "irq_id")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    SECONDS_IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    instance: int
    seconds_irq_id: int
    irq_id: int
    def __init__(self, instance: _Optional[int] = ..., seconds_irq_id: _Optional[int] = ..., irq_id: _Optional[int] = ...) -> None: ...

class RtcSetTimeParams(_message.Message):
    __slots__ = ("instance", "seconds")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    instance: int
    seconds: int
    def __init__(self, instance: _Optional[int] = ..., seconds: _Optional[int] = ...) -> None: ...

class RtcConfAlarmParams(_message.Message):
    __slots__ = ("instance", "time", "rep_interval", "number_of_reps", "repeat_forever", "alarm_int_enable")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    REP_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_REPS_FIELD_NUMBER: _ClassVar[int]
    REPEAT_FOREVER_FIELD_NUMBER: _ClassVar[int]
    ALARM_INT_ENABLE_FIELD_NUMBER: _ClassVar[int]
    instance: int
    time: int
    rep_interval: int
    number_of_reps: int
    repeat_forever: bool
    alarm_int_enable: bool
    def __init__(self, instance: _Optional[int] = ..., time: _Optional[int] = ..., rep_interval: _Optional[int] = ..., number_of_reps: _Optional[int] = ..., repeat_forever: bool = ..., alarm_int_enable: bool = ...) -> None: ...
