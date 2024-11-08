import pytest
from unittest.mock import Mock, patch
from framework.hardware_interfaces.drivers import get_mcan_drv
from framework.hardware_interfaces.drivers.common.definitions.can_buffer import (
    CanBuffer,
)
from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_mcan_driver import (
    MCANDriver,
)
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_mcan_driver_pb2 import (
    MCMsgIdType,
    MCInitParams,
    MCSendParams,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import StatusEnum


@pytest.fixture
def mock_raise_interrupt() -> Mock:
    """Fixture to create a mock function for raise interrupt.

    This function simulates the interrupt functionality.
    """
    return Mock()


@pytest.fixture
def mcan_driver(mock_raise_interrupt: Mock) -> MCANDriver:
    """Fixture to initialize an MCANDriver instance with a mock interrupt function.

    Returns an instance of MCANDriver with a mocked raise interrupt.
    """
    return get_mcan_drv(mock_raise_interrupt)


@pytest.fixture
def can_buffer() -> CanBuffer:
    """Fixture to create a CanBuffer instance.

    Initializes a CanBuffer instance with a specific mbx_id.
    """
    return CanBuffer(mbx_id=1)


def test_get_mcan_drv_returns_instance(mock_raise_interrupt: Mock) -> None:
    """Test that get_mcan_drv function returns an instance of MCANDriver.

    Verifies the returned driver instance and the assigned mock interrupt.
    """
    mcan_driver = get_mcan_drv(mock_raise_interrupt)
    assert isinstance(mcan_driver, MCANDriver)
    assert mcan_driver.raise_interrupt == mock_raise_interrupt


def test_initialize_instance(mcan_driver: MCANDriver) -> None:
    """Test that the _initialize_instance method initializes a driver instance correctly.

    Confirms that the instance and irq_id are correctly registered.
    """
    instance_id, irq_id = 1, 5
    mcan_driver._initialize_instance(instance_id, irq_id)
    assert instance_id in mcan_driver.instances
    assert mcan_driver.instances[instance_id].irq_id == irq_id


def test_get_instance_raises_error_if_not_initialized(mcan_driver: MCANDriver) -> None:
    """Test that get_instance raises a ValueError if the instance is not initialized.

    Ensures that accessing a non-initialized instance raises an appropriate exception.
    """
    with pytest.raises(ValueError):
        mcan_driver.get_instance(instance_id=999)


@patch("framework.support.reports.logger.info")
@patch("framework.support.reports.rpc_call", lambda x: x)
def test_mcan_drv_init(mock_logger: Mock, mcan_driver: MCANDriver) -> None:
    """Test the MCAN_DRV_Init method to ensure it initializes the driver and logs the action.

    Checks successful initialization of the driver and associated logging.
    """
    request = MCInitParams(instance_id=1, irq_id=5)
    context = Mock()
    status = mcan_driver.MCAN_DRV_Init(request, context)

    assert status.status == StatusEnum.STATUS_SUCCESS
    mock_logger.assert_called_with(
        f"MCan driver initialized with IRQ UNKNOWN_IRQn : "
        f"{request.irq_id}, instance {request.instance_id}"
    )


def test_can_buffer_set_mask(can_buffer: CanBuffer) -> None:
    """Test setting the mask on a CanBuffer instance.

    Validates the mask setting on CanBuffer.
    """
    can_buffer.set_mask(0xFF)
    assert can_buffer._mask == 0xFF


def test_can_buffer_set_filter(can_buffer: CanBuffer) -> None:
    """Test setting a message ID filter on a CanBuffer instance.

    Ensures the message ID filter is set correctly on CanBuffer.
    """
    can_buffer.set_filter(0x100)
    assert can_buffer._msg_id == 0x100


def test_can_buffer_check_filter(can_buffer: CanBuffer) -> None:
    """Test that the check_filter method returns True for matching message IDs.

    Checks that check_filter correctly identifies matching message IDs.
    """
    mock_msg = Mock()
    mock_msg.arbitration_id = 0x100
    can_buffer.set_filter(0x100)
    assert can_buffer.check_filter(mock_msg)


def test_can_buffer_put_can_msg_with_filter(can_buffer: CanBuffer) -> None:
    """Test that put_can_msg adds a message to the buffer if it matches the filter.

    Verifies the buffer adds a message when the filter criteria are met.
    """
    mock_msg = Mock()
    mock_msg.arbitration_id = 0x100
    can_buffer.set_filter(0x100)
    result = can_buffer.put_can_msg(mock_msg)
    assert result


@patch("framework.support.reports.rpc_call", lambda x: x)
@patch("framework.support.reports.logger.info")
def test_mcan_driver_send_message(mock_logger: Mock, mcan_driver: MCANDriver) -> None:
    """Test the MCAN_DRV_Send method to ensure messages are sent and logged correctly.

    Confirms message sending and logging functionality for MCAN_DRV_Send.
    """
    init_request = MCInitParams(instance_id=1, irq_id=5)
    context = Mock()
    mcan_driver.MCAN_DRV_Init(init_request, context)

    send_request = MCSendParams(
        instance_id=1,
        msg_id=0x100,
        mb_data=b"\x01\x02",
        msg_id_type=MCMsgIdType.MCMsgIdType_STD,
    )
    status = mcan_driver.MCAN_DRV_Send(send_request, context)

    assert status.status == StatusEnum.STATUS_SUCCESS
    mock_logger.assert_called_with(
        f"Message sent on instance {send_request.instance_id}: "
        f"ID={send_request.msg_id}"
    )


@patch("framework.support.reports.logger.debug")
def test_mcan_driver_wait_for_initialization(
    mock_logger: Mock, mcan_driver: MCANDriver
) -> None:
    """Test the wait_for_initialization method to ensure it waits and logs initialization.

    Verifies correct waiting and logging behavior for driver initialization.
    """
    mcan_driver._ready.set()
    mcan_driver.wait_for_initialization()

    mock_logger.assert_called_with(
        f"Wait for {mcan_driver.__class__.__name__} initialization"
    )
