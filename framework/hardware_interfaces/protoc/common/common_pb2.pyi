from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatusEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATUS_SUCCESS: _ClassVar[StatusEnum]
    STATUS_ERROR: _ClassVar[StatusEnum]
    STATUS_BUSY: _ClassVar[StatusEnum]
    STATUS_TIMEOUT: _ClassVar[StatusEnum]
    STATUS_UNSUPPORTED: _ClassVar[StatusEnum]
STATUS_SUCCESS: StatusEnum
STATUS_ERROR: StatusEnum
STATUS_BUSY: StatusEnum
STATUS_TIMEOUT: StatusEnum
STATUS_UNSUPPORTED: StatusEnum

class Status(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: StatusEnum
    def __init__(self, status: _Optional[_Union[StatusEnum, str]] = ...) -> None: ...
