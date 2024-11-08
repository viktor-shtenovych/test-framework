import socket
import struct
import threading
from enum import IntEnum
from typing import Optional, TypeVar, Type, Any, Generic
from queue import Queue

from framework.communications.uvcs_fluidics.msg_types.ethernet_msgs import (
    BSSDiagnosticsMessage,
    LSDiagnosticsMessage,
    EthernetMessage,
)
from framework.support.reports import logger

T = TypeVar("T", bound="EthernetConn")


class SingletonMeta(Generic[T], type):
    """
    Singleton metaclass.
    """

    _instances: dict[Type[T], T] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T:  # type: ignore
        """
        Call the class.
        """
        with cls._lock:
            if cls._instances.get(cls) is None:
                instance = super().__call__(*args, **kwargs)  # type: ignore
                cls._instances[cls] = instance
        return cls._instances[cls]


class MessageType(IntEnum):
    """
    BSS and Level Sensor message types.
    """

    BSS_DIAGNOSTICS = 0x1C071600
    BSS_FAULT = 0x1C160700
    BSS_READY_REPLY = 0x1D160700
    BSS_READY_REQUEST = 0x1D071600

    LS_DIAGNOSTICS = 0x1C071C00
    LS_FAULT = 0x1C1C0700
    LS_READY_REPLY = 0x1D1C0700
    LS_READY_REQUEST = 0x1D071C00


class EthernetConn(metaclass=SingletonMeta):
    """
    Ethernet connection class.
    """

    def __init__(self, ip: str, port: int) -> None:
        self.ip: str = ip
        self.port: int = port
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))
        self.running: bool = False
        self.listen_thread: Optional[threading.Thread] = None
        self._message_handlers = {
            MessageType.BSS_DIAGNOSTICS: BSSDiagnosticsMessage,
            MessageType.LS_DIAGNOSTICS: LSDiagnosticsMessage,
        }
        self.message_queue: Queue[EthernetMessage] = Queue()

    def start_listening(self) -> None:
        """
        Start listening.
        """
        self.running = True
        self.listen_thread = threading.Thread(target=self._listen)
        self.listen_thread.start()

    def stop_listening(self) -> None:
        """
        Stop listening.
        """
        self.running = False
        # send a dummy packet to unblock the socket
        self.socket.sendto(b"", (self.ip, self.port))
        if self.listen_thread is not None:
            self.listen_thread.join()
            self.listen_thread = None
            self.message_queue = Queue()

    def _listen(self) -> None:
        """
        Listen for messages.
        """
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                if len(data) < 4:
                    continue
                self._handle_message(data, addr)
            except socket.error:
                if not self.running:
                    break

    def _handle_message(self, data: bytes, addr: tuple[str, int]) -> None:
        """
        Handle the message.
        """
        message_id = struct.unpack("!I", data[:4])[0]
        handler = self._message_handlers.get(message_id)
        if handler:
            logger.debug(f"Received message from address {addr}: {handler.__name__}")
            message = handler.unpack(data[4:])
            self.message_queue.put(message)
        else:
            logger.error(f"Unknown message id: {message_id}")

    def send_message(self, message_id: int, data: bytes) -> None:
        """
        Send the message.
        """
        message = struct.pack("!I", message_id) + data
        self.socket.sendto(message, (self.ip, self.port))
