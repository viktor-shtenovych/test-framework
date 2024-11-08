import random
import pytest

from typing import Iterator
from unittest.mock import patch, call
from pytest_mock import MockFixture
from framework.hardware_interfaces.drivers import get_emios_qdec_drv
from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_emios_qdec_driver import (
    BaseEmiosQdecDevice,
)
from framework.hardware_interfaces.protoc.mpc5777c.emios_qdec_driver_pb2 import (
    EmiosQdecParams,
)


@pytest.fixture
def emios_qdec_device(channel: int = 1) -> Iterator[EmiosQdecParams]:
    """
    ! Create a EMIOS device with parameters.

    @param channel: channel number
    @return: Iterator
    """
    emios_qdec_device = EmiosQdecParams()
    emios_qdec_device.mode = 1  # type: ignore
    emios_qdec_device.filter_en = True
    emios_qdec_device.emios_group = 3
    emios_qdec_device.filter_input = 4
    emios_qdec_device.aux_chan_polarity = 5  # type: ignore
    emios_qdec_device.chan_polarity = 6  # type: ignore
    emios_qdec_device.channel = channel

    yield emios_qdec_device


def test_initialize_and_reset_EMIOS_device(mocker: MockFixture) -> None:
    """
    ! Test initialization EMIOS device.

    @return: None
    """
    with patch("framework.support.reports.log.logger.info") as mock_log:
        channels = [1, 3, 17, 21]
        groups = [1, 2, 3, 4]
        channel = random.choice(channels)
        group = random.choice(groups)
        params = EmiosQdecParams(
            emios_group=group,
            channel=channel,
            mode=mocker.MagicMock(),
            filter_input=mocker.MagicMock(),
            aux_chan_polarity=mocker.MagicMock(),
            chan_polarity=mocker.MagicMock(),
        )
        emios_dummy_device = BaseEmiosQdecDevice(group_id=group, channel=channel)
        emios_dummy_device.initialize(params)
        emios_dummy_device.reset()
        assert mock_log.call_args_list == [
            call(f"Initializing Emios device with instance ID: {channel}"),
            call(
                f"Resetting eMIOS QDEC device with instance id: {channel} and group id: {group}"
            ),
        ]


def test_register_and_reset_EMIOS_driver(
    emios_qdec_device: EmiosQdecParams, mocker: MockFixture
) -> None:
    """
    ! Test register and reset EMIOS driver.

    @param emios_qdec_device: EMIOS device
    @param mocker: MockFixture
    @return: None
    """
    with patch("framework.support.reports.log.logger.info") as mock_log:
        interrupt_callback = mocker.MagicMock()
        emios_qdec_driver = get_emios_qdec_drv(interrupt_callback)
        emios_dummy_device = BaseEmiosQdecDevice(
            group_id=emios_qdec_device.emios_group, channel=emios_qdec_device.channel
        )
        emios_qdec_driver.register_device(emios_dummy_device)
        emios_qdec_driver.EMIOS_DRV_QDEC_Init_and_Reset(emios_qdec_device, None)
        assert mock_log.call_args_list == [
            call(
                f"Initializing Emios device with instance ID: {emios_qdec_device.channel}"
            ),
            call(
                f"Resetting eMIOS QDEC device with instance id: {emios_qdec_device.channel} and group id: {emios_qdec_device.emios_group}"
            ),
            call(
                f"Emios QDEC device {emios_qdec_device.channel} initialized and reset."
            ),
        ]
