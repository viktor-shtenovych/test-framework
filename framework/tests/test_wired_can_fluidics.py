import pytest
from unittest.mock import MagicMock, patch

from framework.communications.uvcs_fluidics.fluidics_can import BarcodeReaderScanReply
from framework.apps.fluidics import Fluidics
from framework.simulators.fluidics_simulator import FluidicsSimulator
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    CanMessage,
)


@pytest.fixture
def simulator() -> FluidicsSimulator:
    """
    Create a simulator.
    """
    with patch(
        "framework.simulators.fluidics_simulator.FluidicsSimulator.__init__",
        lambda self, rpc_listening_port: None,
    ):
        sim = FluidicsSimulator(rpc_listening_port=50051)
        sim.can_node = MagicMock()
        sim.irq_manager = MagicMock()
        sim.hw_board = MagicMock()
        sim.async_interface = MagicMock()

        return sim


@pytest.fixture
def fluidics(simulator: FluidicsSimulator) -> Fluidics:
    """
    Create a fluidisc.
    """
    return Fluidics.create_from_sim(simulator)


def test_barcode_reader_scan_reply(
    simulator: FluidicsSimulator, fluidics: Fluidics
) -> None:
    """
    Test Barcode Reader Scan Reply.
    """
    status_data = (
        b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17"
    )
    msg = CanMessage(arbitration_id=0x1C1E0806, data=status_data)
    simulator.can_node.recv.return_value = msg  # type: ignore

    status = fluidics.wired_conn.get_barcode_reader_scan_reply()
    assert isinstance(status, BarcodeReaderScanReply)
    assert status.scan_result == BarcodeReaderScanReply.unpack(status_data).scan_result
