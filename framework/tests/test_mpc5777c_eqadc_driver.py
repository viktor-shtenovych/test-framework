"""! @Brief Test for MPC5777C EQADC driver."""
#
# @file test_mpc5777c_eqadc_driver.py
#
# @section description_test_mpc5777c_eqadc_driver Description
# This module represents the MPC5777C EQADC driver testing.
#
# @section libraries_test_mpc5777c_eqadc_driver Libraries/Modules
# - pytest test framework
# - unittest standard library
# - mpc5777c_eqadc_driver module (local)
#   - Access to BaseEqAdcDevice class.
#   - Access to EqAdcDriver class.
# - common_pb2 module (local)
#   - Access to StatusEnum class.
# - mpc5777c_eqadc_driver_pb2 module (local)
#   - Access to EqAdcConfig class.
#   - Access to EqAdcInitParams class.
#   - Access to EqAdcCCSamplesRequestParams class.
#   - Access to EqAdcCcCalibrateConverterParams class.
#
# @section notes_test_mpc5777c_eqadc_driver Notes
# - None.
#
# @section todo_test_mpc5777c_eqadc_driver TODO
# - None.
#
# @section author_test_mpc5777c_eqadc_driver Author(s)
# - Created by:
#   - Maksym Masalov maksym.masalov@globallogic.com on 06/11/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.

import pytest
from unittest.mock import MagicMock, patch, Mock
from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_eqadc_driver import (
    BaseEqAdcDevice,
    EqAdcDriver,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import StatusEnum
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_eqadc_driver_pb2 import (
    EqAdcConfig,
    EqAdcInitParams,
    EqAdcCCSamplesRequestParams,
    EqAdcCcCalibrateConverterParams,
)


class TestBaseEqAdcDevice:
    """! TestBaseEqAdcDevice testing class."""

    @pytest.fixture(autouse=True)
    def setup_device(self) -> None:
        """! Fixture to set up a BaseEqAdcDevice instance for each test."""
        self.device = BaseEqAdcDevice(instance_id=1)
        self.init_params = EqAdcInitParams(
            samples_num=10,
            adc_config=[EqAdcConfig(gain=1, offset=0)],
            adc_commands=[],
            irq_id=5,
        )

    def test_initialize(self) -> None:
        """! Device initialization check test."""
        self.device.initialize(self.init_params)
        assert self.device.initialized
        assert self.device.sample_num == 10
        assert self.device.adc_config[0].gain == 1
        assert self.device.adc_config[0].offset == 0
        assert self.device.irq_id == 5

    def test_calibrate_converter(self) -> None:
        """! Test to check the calibration of the converter."""
        self.device.initialize(self.init_params)
        self.device.calibrate_converter(
            gain=2, offset=3, rais_interrupt_callback=MagicMock()
        )
        assert self.device.calibrated
        assert self.device.adc_config[0].gain == 2
        assert self.device.adc_config[0].offset == 3


class TestEqAdcDriver:
    """! TestEqAdcDriver testing class."""

    @pytest.fixture(autouse=True)
    def setup_driver(self) -> None:
        """! Fixture to set up an EqAdcDriver instance and a mock interrupt function for each test."""
        self.interrupt_mock = MagicMock()
        self.driver = EqAdcDriver(raise_interrupt_func=self.interrupt_mock)
        self.init_params = EqAdcInitParams(
            instance_id=1,
            samples_num=10,
            adc_config=[EqAdcConfig(gain=1, offset=0)],
            adc_commands=[],
            irq_id=5,
        )

    @patch("framework.support.reports.logger.debug")
    def test_initialize_device(self, mock_logger: Mock) -> None:
        """! Device initialization check test."""
        self.driver._initialize_device(self.init_params)
        assert 1 in self.driver.devices
        assert self.driver.devices[1].initialized
        mock_logger.assert_called_with(
            "New EQADC device 1 created with IRQ UNKNOWN_IRQn : 5"
        )

    def test_get_device(self) -> None:
        """! The test verifies that the device has been received."""
        self.driver._initialize_device(self.init_params)
        device = self.driver.get_device(1)
        assert device.instance_id == 1

    def test_get_device_not_initialized(self) -> None:
        """! The test checks that the device is not initialized."""
        with pytest.raises(ValueError):
            self.driver.get_device(1)

    @patch("framework.support.reports.logger.debug")
    def test_wait_for_initialization(self, mock_logger: Mock) -> None:
        """! The test checks the waiting for device initialization."""
        self.driver._ready.set()
        self.driver.wait_for_initialization()
        mock_logger.assert_called_with("Wait for EQADC driver initialization")

    def test_eqadc_drv_cc_init(self) -> None:
        """! The test checks the driver initialization."""
        status = self.driver.EQADC_DRV_CC_Init(self.init_params, context=None)
        assert status.status == StatusEnum.STATUS_SUCCESS
        assert self.driver._ready.is_set()

    def test_eqadc_drv_cc_calibrate_converter(self) -> None:
        """! The test checks the driver calibration."""
        self.driver._initialize_device(self.init_params)
        calibration_params = EqAdcCcCalibrateConverterParams(
            instance_id=1, gain=5, offset=3
        )
        status = self.driver.EQADC_DRV_CC_CalibrateConverter(
            calibration_params, context=None
        )
        assert status.status == StatusEnum.STATUS_SUCCESS
        assert self.driver.devices[1].adc_config[0].gain == 5
        assert self.driver.devices[1].adc_config[0].offset == 3

    def test_eqadc_drv_cc_samples_request(self) -> None:
        """! The test checks Request Samples."""
        request_params = EqAdcCCSamplesRequestParams(instance_id=1, channel_id=[1, 2])
        self.driver._initialize_device(self.init_params)
        self.driver.EQADC_DRV_CC_SamplesRequest(request_params, context=None)
        assert self.interrupt_mock.called
