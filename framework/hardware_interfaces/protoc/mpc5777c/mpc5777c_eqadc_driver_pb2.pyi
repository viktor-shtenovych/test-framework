import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EqAdcConfig(_message.Message):
    __slots__ = ("adc_id", "prescaler", "gain", "offset")
    ADC_ID_FIELD_NUMBER: _ClassVar[int]
    PRESCALER_FIELD_NUMBER: _ClassVar[int]
    GAIN_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    adc_id: int
    prescaler: int
    gain: int
    offset: int
    def __init__(self, adc_id: _Optional[int] = ..., prescaler: _Optional[int] = ..., gain: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class EqAdcCommand(_message.Message):
    __slots__ = ("channel_id", "sampling_time", "enable_calib", "enable_sign", "pause")
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    SAMPLING_TIME_FIELD_NUMBER: _ClassVar[int]
    ENABLE_CALIB_FIELD_NUMBER: _ClassVar[int]
    ENABLE_SIGN_FIELD_NUMBER: _ClassVar[int]
    PAUSE_FIELD_NUMBER: _ClassVar[int]
    channel_id: int
    sampling_time: int
    enable_calib: bool
    enable_sign: bool
    pause: bool
    def __init__(self, channel_id: _Optional[int] = ..., sampling_time: _Optional[int] = ..., enable_calib: bool = ..., enable_sign: bool = ..., pause: bool = ...) -> None: ...

class EqAdcInitParams(_message.Message):
    __slots__ = ("instance_id", "samples_num", "adc_config", "adc_commands", "irq_id")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    SAMPLES_NUM_FIELD_NUMBER: _ClassVar[int]
    ADC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ADC_COMMANDS_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    samples_num: int
    adc_config: _containers.RepeatedCompositeFieldContainer[EqAdcConfig]
    adc_commands: _containers.RepeatedCompositeFieldContainer[EqAdcCommand]
    irq_id: int
    def __init__(self, instance_id: _Optional[int] = ..., samples_num: _Optional[int] = ..., adc_config: _Optional[_Iterable[_Union[EqAdcConfig, _Mapping]]] = ..., adc_commands: _Optional[_Iterable[_Union[EqAdcCommand, _Mapping]]] = ..., irq_id: _Optional[int] = ...) -> None: ...

class EqAdcCcCalibrateConverterParams(_message.Message):
    __slots__ = ("instance_id", "gain", "offset")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    GAIN_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    gain: int
    offset: int
    def __init__(self, instance_id: _Optional[int] = ..., gain: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class EqAdcCCSamplesRequestParams(_message.Message):
    __slots__ = ("instance_id", "channel_id")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    channel_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, instance_id: _Optional[int] = ..., channel_id: _Optional[_Iterable[int]] = ...) -> None: ...
