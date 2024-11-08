import threading
from collections.abc import Generator

import pytest
from unittest.mock import patch, MagicMock
import struct
from framework.communications.uvcs_fluidics.ethernet_conn import (
    EthernetConn,
    MessageType,
)
from framework.communications.uvcs_fluidics.msg_types.ethernet_msgs import (
    BSSDiagnosticsMessage,
    LSDiagnosticsMessage,
)


@pytest.fixture
def ethernet_conn() -> Generator[EthernetConn, None, None]:
    """
    Ethernet connection fixture.
    """
    conn = EthernetConn("127.0.0.1", 5005)
    yield conn
    conn.stop_listening()
    while not conn.message_queue.empty():
        conn.message_queue.get()


def test_singleton(ethernet_conn: EthernetConn) -> None:
    """
    Test singleton.
    """
    conn1 = EthernetConn("127.0.0.1", 5005)
    conn2 = EthernetConn("127.0.0.1", 5005)
    assert conn1 is conn2


@patch.object(EthernetConn, "_listen", return_value=None)
def test_start_listening(mock_listen: MagicMock, ethernet_conn: EthernetConn) -> None:
    """
    Test start listening.
    """
    ethernet_conn.start_listening()
    assert ethernet_conn.running is True
    assert ethernet_conn.listen_thread is not None


def test_stop_listening(ethernet_conn: EthernetConn) -> None:
    """
    Test stop listening.
    """
    ethernet_conn.start_listening()
    ethernet_conn.stop_listening()
    assert ethernet_conn.running is False
    assert ethernet_conn.listen_thread is None


@patch("socket.socket.recvfrom")
def test_handle_message_bss(
    mock_recvfrom: MagicMock, ethernet_conn: EthernetConn
) -> None:
    """
    Test handle message.
    """
    message_id = MessageType.BSS_DIAGNOSTICS
    fault_id, param1, param2, param3, param4 = 1, 2, 3, 4, 5
    filename = b"filename"
    line_num = 100
    filename_bytes = filename + b"\x00" * (30 - len(filename))
    mock_data = struct.pack(
        "!I4I30sH", fault_id, param1, param2, param3, param4, filename_bytes, line_num
    )
    mock_recvfrom.return_value = (
        struct.pack("!I", message_id) + mock_data,
        ("127.0.0.1", 5005),
    )
    event = threading.Event()

    def wrapped_listen() -> None:
        ethernet_conn.start_listening()
        event.set()

    thread = threading.Thread(target=wrapped_listen)
    thread.start()
    event.wait()

    message = ethernet_conn.message_queue.get_nowait()
    assert isinstance(message, BSSDiagnosticsMessage)
    assert message.fault_id == fault_id
    assert message.param1 == param1
    assert message.param2 == param2
    assert message.param3 == param3
    assert message.param4 == param4
    assert message.filename == "filename"
    assert message.line_num == line_num


@patch("socket.socket.recvfrom")
def test_handle_message_ls(
    mock_recvfrom: MagicMock, ethernet_conn: EthernetConn
) -> None:
    """
    Test handle message.
    """
    message_id = MessageType.LS_DIAGNOSTICS
    fault_id, param1, param2, param3, param4 = 1, 2, 3, 4, 5
    filename = b"filename"
    line_num = 100
    filename_bytes = filename + b"\x00" * (30 - len(filename))
    mock_data = struct.pack(
        "!I4I30sH", fault_id, param1, param2, param3, param4, filename_bytes, line_num
    )
    mock_message = struct.pack("!I", message_id) + mock_data
    mock_recvfrom.return_value = (mock_message, ("127.0.0.1", 5005))

    event = threading.Event()

    def wrapped_listen() -> None:
        ethernet_conn.start_listening()
        event.set()

    thread = threading.Thread(target=wrapped_listen)
    thread.start()
    event.wait()

    while ethernet_conn.message_queue.empty():
        pass

    message = ethernet_conn.message_queue.get_nowait()
    assert isinstance(message, LSDiagnosticsMessage)
    assert message.fault_id == fault_id
    assert message.param1 == param1
    assert message.param2 == param2
    assert message.param3 == param3
    assert message.param4 == param4
    assert message.filename == "filename"
    assert message.line_num == line_num


@patch("socket.socket.sendto")
def test_send_message(mock_sendto: MagicMock, ethernet_conn: EthernetConn) -> None:
    """
    Test send message.
    """
    message_id = MessageType.BSS_DIAGNOSTICS
    data = b"\x01\x02\x03\x04"
    ethernet_conn.send_message(message_id, data)
    packed_data = struct.pack("!I", message_id) + data
    mock_sendto.assert_called_once_with(
        packed_data, (ethernet_conn.ip, ethernet_conn.port)
    )
