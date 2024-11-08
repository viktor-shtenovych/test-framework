import struct
from framework.communications.uvcs_fluidics.msg_types.ethernet_msgs import (
    BSSDiagnosticsMessage,
    LSDiagnosticsMessage,
)


def test_bss_diagnostics_message_pack() -> None:
    """
    Test BSS Diagnostics Message pack.
    """
    message = BSSDiagnosticsMessage(1, 2, 3, 4, 5, "filename", 100)
    packed_data = message.pack()
    expected_data = struct.pack(
        "!I4I30sH",
        1,
        2,
        3,
        4,
        5,
        b"filename\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        100,
    )
    assert packed_data == expected_data


def test_bss_diagnostics_message_unpack() -> None:
    """
    Test BSS Diagnostics Message unpack.
    """
    data = struct.pack(
        "!I4I30sH",
        1,
        2,
        3,
        4,
        5,
        b"filename\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        100,
    )
    message = BSSDiagnosticsMessage.unpack(data)
    assert message.fault_id == 1
    assert message.param1 == 2
    assert message.param2 == 3
    assert message.param3 == 4
    assert message.param4 == 5
    assert message.filename == "filename"
    assert message.line_num == 100


def test_ls_diagnostics_message_pack() -> None:
    """
    Test LS Diagnostics Message pack.
    """
    message = LSDiagnosticsMessage(1, 2, 3, 4, 5, "filename", 100)
    packed_data = message.pack()
    expected_data = struct.pack(
        "!I4I30sH",
        1,
        2,
        3,
        4,
        5,
        b"filename\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        100,
    )
    assert packed_data == expected_data


def test_ls_diagnostics_message_unpack() -> None:
    """
    Test LS Diagnostics Message unpack.
    """
    data = struct.pack(
        "!I4I30sH",
        1,
        2,
        3,
        4,
        5,
        b"filename\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        100,
    )
    message = LSDiagnosticsMessage.unpack(data)
    assert message.fault_id == 1
    assert message.param1 == 2
    assert message.param2 == 3
    assert message.param3 == 4
    assert message.param4 == 5
    assert message.filename == "filename"
    assert message.line_num == 100
