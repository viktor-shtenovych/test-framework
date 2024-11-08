import pytest
from typing import Any
from unittest.mock import Mock
from unittest.mock import patch, call

from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.hardware_interfaces.protoc.mpc5777c.emios_mc_driver_pb2 import (
    EmiosMcInitParams,
)
from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_emios_mc_driver import (
    BaseEmiosMcDevice,
    EmiosMcDriver,
)

EMIOUS_GROUP = 1
CHANNEL = 20
MODE = 2
PERIOD = 5
INTERNAL_PRESCALER = 45
INTERNAL_PRESCALER_EN = True
FILTER_INPUT = 394
FILTER_EN = True
TRIGGER_MODE = 67
IRQ_ID = 1


@pytest.fixture
def emois_mc_device() -> BaseEmiosMcDevice:
    """
    ! Create a EMIOS device with parameters.

    @return: BaseEmiosMcDevice
    """
    return BaseEmiosMcDevice(emios_group=EMIOUS_GROUP, channel=CHANNEL)


@pytest.fixture
def emois_mc_driver() -> EmiosMcDriver:
    """
    ! Create a EMIOS driver with parameters.

    @return: EmiosMcDriver
    """
    raise_interrupt_mock: Mock = Mock()
    return EmiosMcDriver(raise_interrupt_func=raise_interrupt_mock)


def test_emois_mc_driver_initialization(
    emois_mc_device: BaseEmiosMcDevice, emois_mc_driver: EmiosMcDriver
) -> None:
    """
    ! Test initialization EMIOS device.

    @return: None
    """
    with patch("framework.support.reports.log.logger.info") as mock_log:
        emois_mc_driver.register_device(emois_mc_device)
        params = EmiosMcInitParams(
            emios_group=EMIOUS_GROUP,
            channel=CHANNEL,
            mode=MODE,  # type: ignore
            period=PERIOD,
            internal_prescaler=INTERNAL_PRESCALER,  # type: ignore
            internal_prescaler_en=INTERNAL_PRESCALER_EN,
            filter_input=FILTER_INPUT,
            filter_en=FILTER_EN,
            trigger_mode=TRIGGER_MODE,  # type: ignore
            irq_id=IRQ_ID,
        )
        context: Any = Mock()
        response: Status = emois_mc_driver.EMIOS_DRV_MC_InitMode(params, context)

        assert response.status == StatusEnum.STATUS_SUCCESS
        assert emois_mc_device.initialized

        assert mock_log.call_args_list == [
            call(
                f"Registered EmiosMcDevice with group {EMIOUS_GROUP}, channel {CHANNEL}"
            ),
            call(f"Timer {CHANNEL} started with period {PERIOD} microseconds."),
            call(
                f"EmiosMcDevice {EMIOUS_GROUP}/{CHANNEL} initialized with mode {MODE}, period {PERIOD}"
            ),
            call(f"EmiosMcDevice {EMIOUS_GROUP}/{CHANNEL} initialized in mode {MODE}"),
        ]

        emois_mc_driver.stop_all()


def test_emois_mc_driver_set_period_value(
    emois_mc_device: BaseEmiosMcDevice, emois_mc_driver: EmiosMcDriver
) -> None:
    """
    ! Test emios mc EMIOS_DRV_MC_SetPeriodValue method.

    @return: None
    """
    with patch("framework.support.reports.log.logger.info") as mock_log:
        emois_mc_driver.register_device(emois_mc_device)
        params = EmiosMcInitParams(
            emios_group=EMIOUS_GROUP,
            channel=CHANNEL,
            mode=MODE,  # type: ignore
            period=PERIOD,
            internal_prescaler=INTERNAL_PRESCALER,  # type: ignore
            internal_prescaler_en=INTERNAL_PRESCALER_EN,
            filter_input=FILTER_INPUT,
            filter_en=FILTER_EN,
            trigger_mode=TRIGGER_MODE,  # type: ignore
            irq_id=IRQ_ID,
        )
        context: Any = Mock()
        emois_mc_driver.EMIOS_DRV_MC_InitMode(params, context)
        response: Status = emois_mc_driver.EMIOS_DRV_MC_SetPeriodValue(params, context)

        assert response.status == StatusEnum.STATUS_SUCCESS
        assert emois_mc_device.initialized

        assert mock_log.call_args_list == [
            call(
                f"Registered EmiosMcDevice with group {EMIOUS_GROUP}, channel {CHANNEL}"
            ),
            call(f"Timer {CHANNEL} started with period {PERIOD} microseconds."),
            call(
                f"EmiosMcDevice {EMIOUS_GROUP}/{CHANNEL} initialized with mode {MODE}, period {PERIOD}"
            ),
            call(f"EmiosMcDevice {EMIOUS_GROUP}/{CHANNEL} initialized in mode {MODE}"),
            call(f"Timer {CHANNEL} is already running, restarting."),
            call(f"Timer {CHANNEL} stopped."),
            call(f"Timer {CHANNEL} started with period {PERIOD} microseconds."),
            call(f"EmiosMcDevice {EMIOUS_GROUP}/{CHANNEL} period set to {PERIOD}"),
        ]

        emois_mc_driver.stop_all()
