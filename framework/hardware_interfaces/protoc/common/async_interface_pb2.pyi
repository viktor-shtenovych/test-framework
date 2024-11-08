import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AIIrqFlags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AIIrqFlags_RX_FULL: _ClassVar[AIIrqFlags]
    AIIrqFlags_TX_EMPTY: _ClassVar[AIIrqFlags]
    AIIrqFlags_END_TRANSFER: _ClassVar[AIIrqFlags]
    AIIrqFlags_ERROR: _ClassVar[AIIrqFlags]
    AIIrqFlags_RX_IDLE_LINE: _ClassVar[AIIrqFlags]
AIIrqFlags_RX_FULL: AIIrqFlags
AIIrqFlags_TX_EMPTY: AIIrqFlags
AIIrqFlags_END_TRANSFER: AIIrqFlags
AIIrqFlags_ERROR: AIIrqFlags
AIIrqFlags_RX_IDLE_LINE: AIIrqFlags

class AIInitParams(_message.Message):
    __slots__ = ("interface_id", "irq_id")
    INTERFACE_ID_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    interface_id: int
    irq_id: int
    def __init__(self, interface_id: _Optional[int] = ..., irq_id: _Optional[int] = ...) -> None: ...

class AIInterfaceId(_message.Message):
    __slots__ = ("interface_id",)
    INTERFACE_ID_FIELD_NUMBER: _ClassVar[int]
    interface_id: int
    def __init__(self, interface_id: _Optional[int] = ...) -> None: ...

class AIReadReqParams(_message.Message):
    __slots__ = ("interface_id", "data_size")
    INTERFACE_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_SIZE_FIELD_NUMBER: _ClassVar[int]
    interface_id: int
    data_size: int
    def __init__(self, interface_id: _Optional[int] = ..., data_size: _Optional[int] = ...) -> None: ...

class AIGetReadDataReturn(_message.Message):
    __slots__ = ("status", "data_bytes")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_BYTES_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    data_bytes: bytes
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., data_bytes: _Optional[bytes] = ...) -> None: ...

class AIWriteReqParams(_message.Message):
    __slots__ = ("interface_id", "data_bytes")
    INTERFACE_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_BYTES_FIELD_NUMBER: _ClassVar[int]
    interface_id: int
    data_bytes: bytes
    def __init__(self, interface_id: _Optional[int] = ..., data_bytes: _Optional[bytes] = ...) -> None: ...
