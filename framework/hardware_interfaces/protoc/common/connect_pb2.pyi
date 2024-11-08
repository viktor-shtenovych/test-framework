import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CloseRequestEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FSW_CLOSE_REQ_RESET: _ClassVar[CloseRequestEnum]
    FSW_CLOSE_REQ_CRITICAL_ERROR: _ClassVar[CloseRequestEnum]
FSW_CLOSE_REQ_RESET: CloseRequestEnum
FSW_CLOSE_REQ_CRITICAL_ERROR: CloseRequestEnum

class HandShakeRequest(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class HandShakeReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class CloseRequest(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: CloseRequestEnum
    def __init__(self, code: _Optional[_Union[CloseRequestEnum, str]] = ...) -> None: ...

class CloseReply(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _common_pb2.Status
    def __init__(self, status: _Optional[_Union[_common_pb2.Status, _Mapping]] = ...) -> None: ...
