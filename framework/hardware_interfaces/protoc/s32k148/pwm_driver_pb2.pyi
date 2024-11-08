import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PDPolarity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PDPolarity_LOW: _ClassVar[PDPolarity]
    PDPolarity_HIGH: _ClassVar[PDPolarity]
PDPolarity_LOW: PDPolarity
PDPolarity_HIGH: PDPolarity

class PDInitParams(_message.Message):
    __slots__ = ("instance_id", "channel_id", "polarity")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    POLARITY_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    channel_id: int
    polarity: PDPolarity
    def __init__(self, instance_id: _Optional[int] = ..., channel_id: _Optional[int] = ..., polarity: _Optional[_Union[PDPolarity, str]] = ...) -> None: ...

class PDSetPeriodParams(_message.Message):
    __slots__ = ("instance_id", "period")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    period: int
    def __init__(self, instance_id: _Optional[int] = ..., period: _Optional[int] = ...) -> None: ...

class PDSetDutyCycleParams(_message.Message):
    __slots__ = ("instance_id", "channel_id", "duty_cycle")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    DUTY_CYCLE_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    channel_id: int
    duty_cycle: int
    def __init__(self, instance_id: _Optional[int] = ..., channel_id: _Optional[int] = ..., duty_cycle: _Optional[int] = ...) -> None: ...
