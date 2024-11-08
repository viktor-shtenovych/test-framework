import pytest
from unittest.mock import MagicMock, patch
from framework.communications.uvcs_footswitch.msg_types.configuration_msg import (
    ConfigurationMsg310,
)
from framework.communications.uvcs_footswitch.msg_types.real_time_status_msgs import (
    StatusMsg210,
    StatusMsg211,
    StatusMsg212,
)
from framework.apps.footswitch import FootSwitch
from framework.simulators.footswitch_simulator import FootSwitchSimulator
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    CanMessage,
)


@pytest.fixture
def simulator() -> FootSwitchSimulator:
    """
    Create a simulator.
    """
    with patch(
        "framework.simulators.footswitch_simulator.FootSwitchSimulator.__init__",
        lambda self, rpc_listening_port: None,
    ):
        sim = FootSwitchSimulator(rpc_listening_port=50051)
        sim.can_node = MagicMock()
        sim.pins = MagicMock()
        sim.hw_board = MagicMock()
        sim.irq_manager = MagicMock()
        sim.encoder = MagicMock()
        sim.battery1 = MagicMock()
        sim.battery2 = MagicMock()
        sim.adc_driver = MagicMock()
        sim.motor_dac = MagicMock()
        sim.led_driver_adp8866 = MagicMock()
        sim.accelerometer_adxl346 = MagicMock()
        sim.async_interface = MagicMock()
        return sim


@pytest.fixture
def footswitch(simulator: FootSwitchSimulator) -> FootSwitch:
    """
    Create a footswitch.
    """
    return FootSwitch.create_from_sim(simulator)


def test_send_config(footswitch: FootSwitch) -> None:
    """
    Test send config 310.
    """
    config = ConfigurationMsg310(
        newest_supported_proto_version=255,
        oldest_supported_proto_version=1,
        channel_number=10,
        modem_tx_power_attenuation=0,
        console_network_id=12345,
        pairing_info_valid=True,
        console_type=1,
        modem_tx_power_level=1,
    )
    footswitch.wired_conn.send_config(config)
    sent_message = footswitch.wired_conn._bus.send.call_args[0][0]  # type: ignore
    assert sent_message.arbitration_id == 0x310
    assert sent_message.data == config.pack()


def test_get_status_210(simulator: FootSwitchSimulator, footswitch: FootSwitch) -> None:
    """
    Test get status 210.
    """
    status_data = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    msg = CanMessage(arbitration_id=0x210, data=status_data)
    simulator.can_node.recv.return_value = msg  # type: ignore

    status = footswitch.wired_conn.get_status_210()
    assert isinstance(status, StatusMsg210)
    assert status.foot_switch_type == StatusMsg210.unpack(status_data).foot_switch_type


def test_get_status_211(simulator: FootSwitchSimulator, footswitch: FootSwitch) -> None:
    """
    Test get status 211.
    """
    status_data = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    msg = CanMessage(arbitration_id=0x211, data=status_data)
    simulator.can_node.recv.return_value = msg  # type: ignore

    status = footswitch.wired_conn.get_status_211()
    assert isinstance(status, StatusMsg211)
    assert status.aux_type == StatusMsg211.unpack(status_data).aux_type


def test_get_status_212(simulator: FootSwitchSimulator, footswitch: FootSwitch) -> None:
    """
    Test get status 212.
    """
    status_data = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    msg = CanMessage(arbitration_id=0x212, data=status_data)
    simulator.can_node.recv.return_value = msg  # type: ignore

    status = footswitch.wired_conn.get_status_212()
    assert isinstance(status, StatusMsg212)
    assert (
        status.newest_supported_proto_version
        == StatusMsg212.unpack(status_data).newest_supported_proto_version
    )
