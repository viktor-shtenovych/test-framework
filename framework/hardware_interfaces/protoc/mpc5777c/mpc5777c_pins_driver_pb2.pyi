import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PinSettingConfig(_message.Message):
    __slots__ = ("pin_id", "init_value", "mux", "output_mux_enable", "input_mux_enable")
    PIN_ID_FIELD_NUMBER: _ClassVar[int]
    INIT_VALUE_FIELD_NUMBER: _ClassVar[int]
    MUX_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_MUX_ENABLE_FIELD_NUMBER: _ClassVar[int]
    INPUT_MUX_ENABLE_FIELD_NUMBER: _ClassVar[int]
    pin_id: int
    init_value: int
    mux: int
    output_mux_enable: bool
    input_mux_enable: bool
    def __init__(self, pin_id: _Optional[int] = ..., init_value: _Optional[int] = ..., mux: _Optional[int] = ..., output_mux_enable: bool = ..., input_mux_enable: bool = ...) -> None: ...

class ConfigMuxParams(_message.Message):
    __slots__ = ("pin_id", "enable", "mux")
    PIN_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    MUX_FIELD_NUMBER: _ClassVar[int]
    pin_id: int
    enable: bool
    mux: int
    def __init__(self, pin_id: _Optional[int] = ..., enable: bool = ..., mux: _Optional[int] = ...) -> None: ...

class PinReadParams(_message.Message):
    __slots__ = ("pin_id",)
    PIN_ID_FIELD_NUMBER: _ClassVar[int]
    pin_id: int
    def __init__(self, pin_id: _Optional[int] = ...) -> None: ...

class PinWriteParams(_message.Message):
    __slots__ = ("pin_id", "value")
    PIN_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    pin_id: int
    value: int
    def __init__(self, pin_id: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...

class PinsInitParams(_message.Message):
    __slots__ = ("irq_id", "config")
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    irq_id: int
    config: _containers.RepeatedCompositeFieldContainer[PinSettingConfig]
    def __init__(self, irq_id: _Optional[int] = ..., config: _Optional[_Iterable[_Union[PinSettingConfig, _Mapping]]] = ...) -> None: ...

class PinReadReturn(_message.Message):
    __slots__ = ("status", "value")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    value: int
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., value: _Optional[int] = ...) -> None: ...
