import common_pb2 as _common_pb2
import emios_common_pb2 as _emios_common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EmiosQdecMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EmiosQdecMode_ZERO: _ClassVar[EmiosQdecMode]
    EmiosQdecMode_DIRECTION: _ClassVar[EmiosQdecMode]
    EmiosQdecMode_PHASE: _ClassVar[EmiosQdecMode]

class EmiosPulsePolarityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EmiosPulsePolarityType_NEGATIVE: _ClassVar[EmiosPulsePolarityType]
    EmiosPulsePolarityType_POSITIVE: _ClassVar[EmiosPulsePolarityType]
EmiosQdecMode_ZERO: EmiosQdecMode
EmiosQdecMode_DIRECTION: EmiosQdecMode
EmiosQdecMode_PHASE: EmiosQdecMode
EmiosPulsePolarityType_NEGATIVE: EmiosPulsePolarityType
EmiosPulsePolarityType_POSITIVE: EmiosPulsePolarityType

class EmiosQdecParams(_message.Message):
    __slots__ = ("emios_group", "channel", "mode", "filter_input", "filter_en", "chan_polarity", "aux_chan_polarity", "irq_id")
    EMIOS_GROUP_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    FILTER_INPUT_FIELD_NUMBER: _ClassVar[int]
    FILTER_EN_FIELD_NUMBER: _ClassVar[int]
    CHAN_POLARITY_FIELD_NUMBER: _ClassVar[int]
    AUX_CHAN_POLARITY_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    emios_group: int
    channel: int
    mode: EmiosQdecMode
    filter_input: _emios_common_pb2.EmiosInputFilterType
    filter_en: bool
    chan_polarity: EmiosPulsePolarityType
    aux_chan_polarity: EmiosPulsePolarityType
    irq_id: int
    def __init__(self, emios_group: _Optional[int] = ..., channel: _Optional[int] = ..., mode: _Optional[_Union[EmiosQdecMode, str]] = ..., filter_input: _Optional[_Union[_emios_common_pb2.EmiosInputFilterType, str]] = ..., filter_en: bool = ..., chan_polarity: _Optional[_Union[EmiosPulsePolarityType, str]] = ..., aux_chan_polarity: _Optional[_Union[EmiosPulsePolarityType, str]] = ..., irq_id: _Optional[int] = ...) -> None: ...

class EmiosQdecTargetParams(_message.Message):
    __slots__ = ("emios_group", "channel", "target")
    EMIOS_GROUP_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    emios_group: int
    channel: int
    target: int
    def __init__(self, emios_group: _Optional[int] = ..., channel: _Optional[int] = ..., target: _Optional[int] = ...) -> None: ...
