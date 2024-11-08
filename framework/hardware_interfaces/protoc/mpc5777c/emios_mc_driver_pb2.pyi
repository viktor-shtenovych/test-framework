import common_pb2 as _common_pb2
import emios_common_pb2 as _emios_common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EmiosMcMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EMIOS_MODE_MC_ZERO: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MC_UP_CNT_CLR_START_INT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MC_UP_CNT_CLR_START_EXT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MC_UP_CNT_CLR_END_INT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MC_UP_CNT_CLR_END_EXT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MC_UPDOWN_CNT_FLAGX1_INT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MC_UPDOWN_CNT_FLAGX1_EXT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MC_UPDOWN_CNT_FLAGX2_INT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MC_UPDOWN_CNT_FLAGX2_EXT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MCB_UP_COUNTER_INT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MCB_UP_COUNTER_EXT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MCB_UPDOWN_CNT_FLAGX1_INT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MCB_UPDOWN_CNT_FLAGX1_EXT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MCB_UPDOWN_CNT_FLAGX2_INT_CLK: _ClassVar[EmiosMcMode]
    EMIOS_MODE_MCB_UPDOWN_CNT_FLAGX2_EXT_CLK: _ClassVar[EmiosMcMode]

class EmiosClockInternalPsType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EMIOS_CLOCK_DIVID_BY_1: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_2: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_3: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_4: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_5: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_6: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_7: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_8: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_9: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_10: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_11: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_12: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_13: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_14: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_15: _ClassVar[EmiosClockInternalPsType]
    EMIOS_CLOCK_DIVID_BY_16: _ClassVar[EmiosClockInternalPsType]

class EmiosEdgeTriggerMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EMIOS_TRIGGER_EDGE_FALLING: _ClassVar[EmiosEdgeTriggerMode]
    EMIOS_TRIGGER_EDGE_RISING: _ClassVar[EmiosEdgeTriggerMode]
    EMIOS_TRIGGER_EDGE_ANY: _ClassVar[EmiosEdgeTriggerMode]
EMIOS_MODE_MC_ZERO: EmiosMcMode
EMIOS_MODE_MC_UP_CNT_CLR_START_INT_CLK: EmiosMcMode
EMIOS_MODE_MC_UP_CNT_CLR_START_EXT_CLK: EmiosMcMode
EMIOS_MODE_MC_UP_CNT_CLR_END_INT_CLK: EmiosMcMode
EMIOS_MODE_MC_UP_CNT_CLR_END_EXT_CLK: EmiosMcMode
EMIOS_MODE_MC_UPDOWN_CNT_FLAGX1_INT_CLK: EmiosMcMode
EMIOS_MODE_MC_UPDOWN_CNT_FLAGX1_EXT_CLK: EmiosMcMode
EMIOS_MODE_MC_UPDOWN_CNT_FLAGX2_INT_CLK: EmiosMcMode
EMIOS_MODE_MC_UPDOWN_CNT_FLAGX2_EXT_CLK: EmiosMcMode
EMIOS_MODE_MCB_UP_COUNTER_INT_CLK: EmiosMcMode
EMIOS_MODE_MCB_UP_COUNTER_EXT_CLK: EmiosMcMode
EMIOS_MODE_MCB_UPDOWN_CNT_FLAGX1_INT_CLK: EmiosMcMode
EMIOS_MODE_MCB_UPDOWN_CNT_FLAGX1_EXT_CLK: EmiosMcMode
EMIOS_MODE_MCB_UPDOWN_CNT_FLAGX2_INT_CLK: EmiosMcMode
EMIOS_MODE_MCB_UPDOWN_CNT_FLAGX2_EXT_CLK: EmiosMcMode
EMIOS_CLOCK_DIVID_BY_1: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_2: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_3: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_4: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_5: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_6: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_7: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_8: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_9: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_10: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_11: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_12: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_13: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_14: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_15: EmiosClockInternalPsType
EMIOS_CLOCK_DIVID_BY_16: EmiosClockInternalPsType
EMIOS_TRIGGER_EDGE_FALLING: EmiosEdgeTriggerMode
EMIOS_TRIGGER_EDGE_RISING: EmiosEdgeTriggerMode
EMIOS_TRIGGER_EDGE_ANY: EmiosEdgeTriggerMode

class EmiosMcInitParams(_message.Message):
    __slots__ = ("emios_group", "channel", "mode", "period", "internal_prescaler", "internal_prescaler_en", "filter_input", "filter_en", "trigger_mode", "irq_id")
    EMIOS_GROUP_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_PRESCALER_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_PRESCALER_EN_FIELD_NUMBER: _ClassVar[int]
    FILTER_INPUT_FIELD_NUMBER: _ClassVar[int]
    FILTER_EN_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_MODE_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    emios_group: int
    channel: int
    mode: EmiosMcMode
    period: int
    internal_prescaler: EmiosClockInternalPsType
    internal_prescaler_en: bool
    filter_input: _emios_common_pb2.EmiosInputFilterType
    filter_en: bool
    trigger_mode: EmiosEdgeTriggerMode
    irq_id: int
    def __init__(self, emios_group: _Optional[int] = ..., channel: _Optional[int] = ..., mode: _Optional[_Union[EmiosMcMode, str]] = ..., period: _Optional[int] = ..., internal_prescaler: _Optional[_Union[EmiosClockInternalPsType, str]] = ..., internal_prescaler_en: bool = ..., filter_input: _Optional[_Union[_emios_common_pb2.EmiosInputFilterType, str]] = ..., filter_en: bool = ..., trigger_mode: _Optional[_Union[EmiosEdgeTriggerMode, str]] = ..., irq_id: _Optional[int] = ...) -> None: ...

class EmiosMcSetPeriodParams(_message.Message):
    __slots__ = ("emios_group", "channel", "period")
    EMIOS_GROUP_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    emios_group: int
    channel: int
    period: int
    def __init__(self, emios_group: _Optional[int] = ..., channel: _Optional[int] = ..., period: _Optional[int] = ...) -> None: ...
