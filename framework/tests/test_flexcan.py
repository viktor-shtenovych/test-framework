from unittest.mock import call

from pytest_mock import MockFixture

from framework.communications.uvcs_footswitch.msg_types.real_time_status_msgs import (
    StatusMsg210,
)
from framework.hardware_interfaces.protoc.common.flexcan_driver_pb2 import (
    FCInitParams,
    FCReceiveReqParams,
    FCConfigRxMbParams,
    FCSetRxIndMaskParams,
    FCGetReceivedDataParams,
    FCIrqFlags,
    FCSendParams,
    FCMsgIdType,
)
from framework.communications.uvcs_footswitch.msg_types.configuration_msg import (
    ConfigurationMsg310,
)
from framework.communications.uvcs_console.wired.wiredconn import WiredConn
from framework.hardware_interfaces.drivers import get_can_bus_drv
from framework.hardware_interfaces.drivers.common.flexcan_driver import FlexCanDriver


def setup_flexcan_drv(
    canbus: FlexCanDriver,
    instance_id: int,
    mb_idx: int,
    irq_id: int,
    msg_id: int | None = None,
) -> None:
    """
    Setup the FlexCAN driver for testing.

    Args:
        canbus (FlexCanDriver): The FlexCAN driver.
        instance_id (int): The instance ID.
        mb_idx (int): The message buffer index.
        irq_id (int): The IRQ ID.
        msg_id (int, optional): The message ID. Defaults to None.
    """
    canbus.FLEXCAN_DRV_Init(
        FCInitParams(instance_id=instance_id, irq_id=irq_id, max_num_mb=255), None
    )
    canbus.FLEXCAN_DRV_SetRxIndividualMask(
        FCSetRxIndMaskParams(instance_id=0, mb_idx=mb_idx), None
    )

    config_params = FCConfigRxMbParams(instance_id=instance_id, mb_idx=mb_idx)
    if msg_id:
        config_params.msg_id = msg_id
    canbus.FLEXCAN_DRV_ConfigRxMb(config_params, None)

    canbus.FLEXCAN_DRV_ReceiveReq(
        FCReceiveReqParams(instance_id=instance_id, mb_idx=mb_idx), None
    )


def test_transfer_data_read(mocker: MockFixture) -> None:
    """
    Test the transfer of data from the CAN bus.
    """
    interrupt_callback = mocker.MagicMock()
    mb_idx = 1
    irq_id = -1
    instance_id = 0

    canbus = get_can_bus_drv(interrupt_callback)
    setup_flexcan_drv(canbus, instance_id, mb_idx, irq_id)

    wired = WiredConn(canbus)
    config_msg = ConfigurationMsg310()
    wired.send_config(config_msg)

    interrupt_callback.assert_called_with(
        irq_id, (mb_idx << 16) | FCIrqFlags.FCIrqFlags_RX_COMPLETE
    )

    data = canbus.FLEXCAN_DRV_GetReceivedData(
        FCGetReceivedDataParams(instance_id=0, mb_idx=mb_idx), None
    )

    assert data.msg_id == 0x310
    assert data.instance_id == 0
    assert data.mb_data == config_msg.pack()


def test_more_buffers_read(mocker: MockFixture) -> None:
    """
    Test the transfer of data from the CAN bus with more than one message buffer.
    """
    interrupt_callback = mocker.MagicMock()
    irq_id = -1
    instance_id = 0

    canbus = get_can_bus_drv(interrupt_callback)

    setup_flexcan_drv(canbus, instance_id, 1, irq_id)
    setup_flexcan_drv(canbus, instance_id, 2, irq_id)

    wired = WiredConn(canbus)
    config_msg = ConfigurationMsg310()
    wired.send_config(config_msg)

    interrupt_callback.assert_has_calls(
        [
            call(irq_id, (2 << 16) | FCIrqFlags.FCIrqFlags_RX_COMPLETE),
            call(irq_id, (1 << 16) | FCIrqFlags.FCIrqFlags_RX_COMPLETE),
        ],
        any_order=True,
    )

    data = canbus.FLEXCAN_DRV_GetReceivedData(
        FCGetReceivedDataParams(instance_id=0, mb_idx=1), None
    )

    assert data.msg_id == 0x310
    assert data.instance_id == 0
    assert data.mb_data == config_msg.pack()

    data = canbus.FLEXCAN_DRV_GetReceivedData(
        FCGetReceivedDataParams(instance_id=0, mb_idx=2), None
    )

    assert data.msg_id == 0x310
    assert data.instance_id == 0
    assert data.mb_data == config_msg.pack()


def test_more_buffers_filter_read(mocker: MockFixture) -> None:
    """
    Test the transfer of data from the CAN bus with more than one message buffer and the same message ID.
    """
    interrupt_callback = mocker.MagicMock()
    irq_id = -1
    instance_id = 0

    canbus = get_can_bus_drv(interrupt_callback)

    setup_flexcan_drv(canbus, instance_id, 1, irq_id, msg_id=0x210)
    setup_flexcan_drv(canbus, instance_id, 2, irq_id, msg_id=0x310)
    setup_flexcan_drv(canbus, instance_id, 3, irq_id, msg_id=0x310)

    wired = WiredConn(canbus)
    config_msg = ConfigurationMsg310()
    wired.send_config(config_msg)

    interrupt_callback.assert_has_calls(
        [
            call(irq_id, (2 << 16) | FCIrqFlags.FCIrqFlags_RX_COMPLETE),
            call(irq_id, (3 << 16) | FCIrqFlags.FCIrqFlags_RX_COMPLETE),
        ],
        any_order=True,
    )

    data = canbus.FLEXCAN_DRV_GetReceivedData(
        FCGetReceivedDataParams(instance_id=0, mb_idx=2), None
    )

    assert data.msg_id == 0x310
    assert data.instance_id == 0
    assert data.mb_data == config_msg.pack()

    data = canbus.FLEXCAN_DRV_GetReceivedData(
        FCGetReceivedDataParams(instance_id=0, mb_idx=3), None
    )

    assert data.msg_id == 0x310
    assert data.instance_id == 0
    assert data.mb_data == config_msg.pack()


def test_transfer_data_write(mocker: MockFixture) -> None:
    """
    Test the transfer of data to the CAN bus.
    """
    interrupt_callback = mocker.MagicMock()
    mb_idx = 1
    irq_id = -1
    instance_id = 0

    canbus = get_can_bus_drv(interrupt_callback)
    setup_flexcan_drv(canbus, instance_id, mb_idx, irq_id)

    data = bytes([0x00, 0x02, 0xFF, 0xAF, 0x0F, 0xFF, 0x0A, 0x00])

    canbus.FLEXCAN_DRV_Send(
        FCSendParams(
            instance_id=0,
            mb_idx=1,
            msg_id_type=FCMsgIdType.FCMsgIdType_STD,
            msg_id=0x210,
            mb_data=data,
        ),
        None,
    )

    wired = WiredConn(canbus)
    msg = wired.await_message(StatusMsg210)
    print(msg)
