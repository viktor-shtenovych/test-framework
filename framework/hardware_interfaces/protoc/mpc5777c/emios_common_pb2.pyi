import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EmiosInputFilterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EMIOS_INPUT_FILTER_BYPASS: _ClassVar[EmiosInputFilterType]
    EMIOS_INPUT_FILTER_02: _ClassVar[EmiosInputFilterType]
    EMIOS_INPUT_FILTER_04: _ClassVar[EmiosInputFilterType]
    EMIOS_INPUT_FILTER_08: _ClassVar[EmiosInputFilterType]
    EMIOS_INPUT_FILTER_16: _ClassVar[EmiosInputFilterType]
EMIOS_INPUT_FILTER_BYPASS: EmiosInputFilterType
EMIOS_INPUT_FILTER_02: EmiosInputFilterType
EMIOS_INPUT_FILTER_04: EmiosInputFilterType
EMIOS_INPUT_FILTER_08: EmiosInputFilterType
EMIOS_INPUT_FILTER_16: EmiosInputFilterType

class EmiosInitGlobalParams(_message.Message):
    __slots__ = ("emios_group", "allow_debug_mode", "low_power_mode", "clk_div_val", "enable_global_prescaler", "enable_global_time_base", "enable_external_time_base", "server_time_slot", "irq_id")
    EMIOS_GROUP_FIELD_NUMBER: _ClassVar[int]
    ALLOW_DEBUG_MODE_FIELD_NUMBER: _ClassVar[int]
    LOW_POWER_MODE_FIELD_NUMBER: _ClassVar[int]
    CLK_DIV_VAL_FIELD_NUMBER: _ClassVar[int]
    ENABLE_GLOBAL_PRESCALER_FIELD_NUMBER: _ClassVar[int]
    ENABLE_GLOBAL_TIME_BASE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_EXTERNAL_TIME_BASE_FIELD_NUMBER: _ClassVar[int]
    SERVER_TIME_SLOT_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    emios_group: int
    allow_debug_mode: bool
    low_power_mode: bool
    clk_div_val: int
    enable_global_prescaler: bool
    enable_global_time_base: bool
    enable_external_time_base: bool
    server_time_slot: int
    irq_id: int
    def __init__(self, emios_group: _Optional[int] = ..., allow_debug_mode: bool = ..., low_power_mode: bool = ..., clk_div_val: _Optional[int] = ..., enable_global_prescaler: bool = ..., enable_global_time_base: bool = ..., enable_external_time_base: bool = ..., server_time_slot: _Optional[int] = ..., irq_id: _Optional[int] = ...) -> None: ...

class EmiosSetPrescalerEnParams(_message.Message):
    __slots__ = ("emios_group", "channel", "value")
    EMIOS_GROUP_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    emios_group: int
    channel: int
    value: bool
    def __init__(self, emios_group: _Optional[int] = ..., channel: _Optional[int] = ..., value: bool = ...) -> None: ...
