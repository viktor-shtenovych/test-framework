import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EtpuI2cInitParams(_message.Message):
    __slots__ = ("instance_id", "irq_id")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    IRQ_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    irq_id: int
    def __init__(self, instance_id: _Optional[int] = ..., irq_id: _Optional[int] = ...) -> None: ...

class EtpuI2cReceiveReqParams(_message.Message):
    __slots__ = ("instance_id", "device_address", "size")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    device_address: int
    size: int
    def __init__(self, instance_id: _Optional[int] = ..., device_address: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class EtpuI2cTransmitParams(_message.Message):
    __slots__ = ("instance_id", "device_address", "message")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    device_address: int
    message: bytes
    def __init__(self, instance_id: _Optional[int] = ..., device_address: _Optional[int] = ..., message: _Optional[bytes] = ...) -> None: ...

class EtpuI2cInterfaceIdParams(_message.Message):
    __slots__ = ("instance_id",)
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: int
    def __init__(self, instance_id: _Optional[int] = ...) -> None: ...

class EtpuI2cGetReceivedDataReturn(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    message: bytes
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ..., message: _Optional[bytes] = ...) -> None: ...
