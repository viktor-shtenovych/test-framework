import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SifInitParams(_message.Message):
    __slots__ = ("instance", "irq_id")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    instance: int
    irq_id: int
    def __init__(self, instance: _Optional[int] = ..., irq_id: _Optional[int] = ...) -> None: ...

class SifReadParams(_message.Message):
    __slots__ = ("instance", "periph_id", "size", "irq_required")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    PERIPH_ID_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    IRQ_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    instance: int
    periph_id: int
    size: int
    irq_required: bool
    def __init__(self, instance: _Optional[int] = ..., periph_id: _Optional[int] = ..., size: _Optional[int] = ..., irq_required: bool = ...) -> None: ...

class SifWriteParams(_message.Message):
    __slots__ = ("instance", "periph_id", "message", "irq_required")
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    PERIPH_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IRQ_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    instance: int
    periph_id: int
    message: bytes
    irq_required: bool
    def __init__(self, instance: _Optional[int] = ..., periph_id: _Optional[int] = ..., message: _Optional[bytes] = ..., irq_required: bool = ...) -> None: ...

class SifReadReturns(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    message: bytes
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., message: _Optional[bytes] = ...) -> None: ...
