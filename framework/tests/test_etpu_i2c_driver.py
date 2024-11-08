import pytest
from unittest.mock import Mock, patch
from typing import Any
from framework.hardware_interfaces.drivers.mpc5777c.etpu_i2c_driver import (
    EtpuI2cDevice,
    EtpuI2cDriver,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.hardware_interfaces.protoc.mpc5777c.etpu_i2c_driver_pb2 import (
    EtpuI2cInitParams,
    EtpuI2cTransmitParams,
    EtpuI2cReceiveReqParams,
    EtpuI2cInterfaceIdParams,
)


@pytest.fixture
def i2c_device() -> EtpuI2cDevice:
    """Fixture to create an I2C device."""
    return EtpuI2cDevice(instance_id=1, address=0x50)


@pytest.fixture
def i2c_driver() -> EtpuI2cDriver:
    """Fixture to create an I2C driver with a mock interrupt function."""
    raise_interrupt_mock: Mock = Mock()
    return EtpuI2cDriver(raise_interrupt_func=raise_interrupt_mock)


def test_etpu_i2c_driver_initialization(
    i2c_driver: EtpuI2cDriver, i2c_device: EtpuI2cDevice
) -> None:
    """Test initialization of the I2C driver."""
    i2c_driver.register_device(i2c_device)
    params = EtpuI2cInitParams(instance_id=1, irq_id=100)
    context: Any = Mock()

    response: Status = i2c_driver.ETPU_I2C_DRV_Init(params, context)

    assert response.status == StatusEnum.STATUS_SUCCESS
    assert i2c_device.initialized


def test_etpu_i2c_driver_transmit(
    i2c_driver: EtpuI2cDriver, i2c_device: EtpuI2cDevice
) -> None:
    """Test data transmission through the I2C driver."""
    i2c_driver.register_device(i2c_device)
    params = EtpuI2cTransmitParams(instance_id=1, message=b"Test Message")
    context: Any = Mock()

    response: Status = i2c_driver.ETPU_I2C_DRV_Transmit(params, context)

    assert response.status == StatusEnum.STATUS_SUCCESS
    assert i2c_device.data == b"Test Message"


def test_etpu_i2c_driver_receive_request(
    i2c_driver: EtpuI2cDriver, i2c_device: EtpuI2cDevice
) -> None:
    """Test receiving data request through the I2C driver."""
    i2c_driver.register_device(i2c_device)
    params = EtpuI2cReceiveReqParams(instance_id=1, device_address=0x50, size=5)
    context: Any = Mock()

    # Mock the _raise_interrupt method
    with patch.object(i2c_driver, "_raise_interrupt") as mock_raise_interrupt:
        response: Status = i2c_driver.ETPU_I2C_DRV_ReceiveReq(params, context)

        # Assert the response is successful
        assert response.status == StatusEnum.STATUS_SUCCESS

        mock_raise_interrupt.assert_called_once_with(i2c_device.irq_id, 0)


def test_etpu_i2c_driver_get_received_data(
    i2c_driver: EtpuI2cDriver, i2c_device: EtpuI2cDevice
) -> None:
    """Test retrieving received data from the I2C driver."""
    i2c_driver.register_device(i2c_device)
    i2c_device.transmit(b"Test Data")
    params = EtpuI2cInterfaceIdParams(instance_id=1)
    context: Any = Mock()  # Added explicit type for context

    # Call the driver function to get received data
    response = i2c_driver.ETPU_I2C_DRV_GetReceivedData(params, context)

    # Assert the status is success
    assert response.status.status == StatusEnum.STATUS_SUCCESS

    # Assert the message matches the transmitted data
    assert response.message == b"Test Data"
