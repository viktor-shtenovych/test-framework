import struct

from abc import ABC, abstractmethod


class EthernetMessage(ABC):
    """
    Ethernet Message.
    """

    @abstractmethod
    def pack(self) -> bytes:
        """
        Pack the Ethernet Message.
        """
        pass

    @classmethod
    @abstractmethod
    def unpack(cls, data: bytes) -> "EthernetMessage":
        """
        Unpack the Ethernet Message.
        """
        pass


class BSSDiagnosticsMessage(EthernetMessage):
    """
    BSS Diagnostics Message.
    """

    message_id = 0x1C071600

    def __init__(
        self,
        fault_id: int,
        param1: int,
        param2: int,
        param3: int,
        param4: int,
        filename: str,
        line_num: int,
    ):
        self.fault_id = fault_id
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4
        self.filename = filename
        self.line_num = line_num

    def pack(self) -> bytes:
        """
        Pack the BSS Diagnostics Message.
        """
        filename_bytes = self.filename.encode("ascii") + b"\x00" * (
            30 - len(self.filename)
        )
        return struct.pack(
            "!I4I30sH",
            self.fault_id,
            self.param1,
            self.param2,
            self.param3,
            self.param4,
            filename_bytes,
            self.line_num,
        )

    @classmethod
    def unpack(cls, data: bytes) -> "BSSDiagnosticsMessage":
        """
        Unpack the BSS Diagnostics Message.
        """
        fault_id, param1, param2, param3, param4, filename_bytes, line_num = (
            struct.unpack("!I4I30sH", data)
        )
        filename = filename_bytes.decode("ascii").rstrip("\x00")
        return cls(fault_id, param1, param2, param3, param4, filename, line_num)


class LSDiagnosticsMessage(EthernetMessage):
    """
    LS Diagnostics Message.
    """

    message_id = 0x1C071C00

    def __init__(
        self,
        fault_id: int,
        param1: int,
        param2: int,
        param3: int,
        param4: int,
        filename: str,
        line_num: int,
    ) -> None:
        self.fault_id = fault_id
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4
        self.filename = filename
        self.line_num = line_num

    def pack(self) -> bytes:
        """
        Pack the LS Diagnostics Message.
        """
        filename_bytes = self.filename.encode("ascii") + b"\x00" * (
            30 - len(self.filename)
        )
        return struct.pack(
            "!I4I30sH",
            self.fault_id,
            self.param1,
            self.param2,
            self.param3,
            self.param4,
            filename_bytes,
            self.line_num,
        )

    @classmethod
    def unpack(cls, data: bytes) -> "LSDiagnosticsMessage":
        """
        Unpack the LS Diagnostics Message.
        """
        fault_id, param1, param2, param3, param4, filename_bytes, line_num = (
            struct.unpack("!I4I30sH", data)
        )
        filename = filename_bytes.decode("ascii").rstrip("\x00")
        return cls(fault_id, param1, param2, param3, param4, filename, line_num)
