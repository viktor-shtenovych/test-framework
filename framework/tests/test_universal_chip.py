import pytest

from framework.core.devices.universal_chip import UniversalChip

DATA = {
    bytes("cmd1", "utf-8"): bytes("response1", "utf-8"),
    bytes([0, 1]): bytes([5, 5, 5, 5]),
}
UNDEFINED_CMD = b"\xff"


def test_cmd_response() -> None:
    """
    Test command response.
    """
    sim_chip = UniversalChip(DATA)

    for request, response in DATA.items():
        sim_chip.write(request)
        assert sim_chip.read() == response
        assert sim_chip.read() == response


def test_no_cmd_exception() -> None:
    """
    Test no command exception.
    """
    sim_chip = UniversalChip(DATA)

    with pytest.raises(RuntimeError):
        sim_chip.read()

    default_response = b"default"
    sim_chip = UniversalChip(DATA, default_response)

    assert sim_chip.read() == default_response


def test_unknown_cmd_exception() -> None:
    """
    Test unknown command exception.
    """
    sim_chip = UniversalChip(DATA)
    sim_chip.write(UNDEFINED_CMD)

    with pytest.raises(KeyError):
        sim_chip.read()


def test_unknown_cmd_default_response() -> None:
    """
    Test unknown command with default response.
    """
    default_response = b"default"
    sim_chip = UniversalChip(DATA, default_response)
    sim_chip.write(UNDEFINED_CMD)

    assert sim_chip.read() == default_response


def test_default_response() -> None:
    """
    Test default response.
    """
    default_response = b"default"
    sim_chip = UniversalChip(DATA, bytes(default_response))
    sim_chip.write(UNDEFINED_CMD)

    assert sim_chip.read() == default_response
