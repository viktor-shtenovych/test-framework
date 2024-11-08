import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Direction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FSW_IN: _ClassVar[Direction]
    FSW_OUT: _ClassVar[Direction]
    FSW_UNDEFINED: _ClassVar[Direction]
FSW_IN: Direction
FSW_OUT: Direction
FSW_UNDEFINED: Direction

class PinSettingConfig(_message.Message):
    __slots__ = ("pin_id", "port_id", "direction", "init_value")
    PIN_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    INIT_VALUE_FIELD_NUMBER: _ClassVar[int]
    pin_id: int
    port_id: int
    direction: Direction
    init_value: int
    def __init__(self, pin_id: _Optional[int] = ..., port_id: _Optional[int] = ..., direction: _Optional[_Union[Direction, str]] = ..., init_value: _Optional[int] = ...) -> None: ...

class PortIrqId(_message.Message):
    __slots__ = ("port_id", "irq_id")
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    port_id: int
    irq_id: int
    def __init__(self, port_id: _Optional[int] = ..., irq_id: _Optional[int] = ...) -> None: ...

class PinSetDirectionParams(_message.Message):
    __slots__ = ("pin_id", "port_id", "direction")
    PIN_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    pin_id: int
    port_id: int
    direction: Direction
    def __init__(self, pin_id: _Optional[int] = ..., port_id: _Optional[int] = ..., direction: _Optional[_Union[Direction, str]] = ...) -> None: ...

class PinWriteParams(_message.Message):
    __slots__ = ("pin_id", "port_id", "value")
    PIN_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    pin_id: int
    port_id: int
    value: int
    def __init__(self, pin_id: _Optional[int] = ..., port_id: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...

class PinsInitParams(_message.Message):
    __slots__ = ("config", "irq_ids")
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    IRQ_IDS_FIELD_NUMBER: _ClassVar[int]
    config: _containers.RepeatedCompositeFieldContainer[PinSettingConfig]
    irq_ids: _containers.RepeatedCompositeFieldContainer[PortIrqId]
    def __init__(self, config: _Optional[_Iterable[_Union[PinSettingConfig, _Mapping]]] = ..., irq_ids: _Optional[_Iterable[_Union[PortIrqId, _Mapping]]] = ...) -> None: ...
