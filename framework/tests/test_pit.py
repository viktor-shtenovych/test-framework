"""! @brief Defines the PIT driver testing."""
##
# @file test_pit.py
#
# @brief Defines the PIT driver testing.
#
# @section description_test_pit Description
# This module representing the PIT driver testing.
#
# @section libraries_test_pit Libraries/Modules
# - pytest standard library (https://pypi.org/project/pytest/)
# - threading standard library (https://docs.python.org/uk/3/library/threading.html)
# - typing standard library (https://docs.python.org/3/library/typing.html)
# - unittest standard library for mock data (https://docs.python.org/3/library/unittest.html)
# - PIT module (local)
#   - Access to Channel class.
#   - Access to PITChannelManager class.
#
# @section notes_test_pit Notes
# - None.
#
# @section todo_test_pit TODO
# - None.
#
# @section author_test_pit Author(s)
# - Created by:
#   - Maksym Masalov <maksym.masalov@globallogic.com> on 10/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic.  All rights reserved.

import pytest

from threading import Thread
from typing import Generator, cast
from unittest.mock import patch, MagicMock, call

from framework.core.control.pit import PITChannelManager
from framework.hardware_interfaces.drivers.common.definitions.channel import Channel


class TestChannel:
    """! Test Channel class."""

    @pytest.fixture
    def channel(self, mocker: MagicMock) -> Generator[Channel, None, None]:
        """! Create a Channel."""
        mocker.patch("threading.Thread")
        _channel: Channel = Channel(channel_id=1)
        yield _channel

    def test_channel_start_already_running(
        self, channel: Channel, mocker: MagicMock
    ) -> None:
        """! Test start method when channel is already running.

        @param channel: Channel.
        @param mocker: Mocking framework.
        """
        channel._timer_thread = cast(MagicMock, mocker.MagicMock(spec=Thread))
        if channel._timer_thread is not None:
            channel._timer_thread.is_alive.return_value = True
            with patch("framework.support.reports.log.logger.info") as mock_log:
                channel.start()
                assert mock_log.call_args_list == [
                    call("Timer 1 is already running, restarting."),
                    call("Timer 1 started with period 1 microseconds."),
                ]
                channel.stop()

    def test_channel_stop_not_running(self, channel: Channel) -> None:
        """! Test stop method when channel is not running."""
        with patch("framework.support.reports.log.logger.debug") as mock_log:
            channel.stop()
            mock_log.assert_called_once_with("Timer 1 is not running.")

    def test_channel_start_stop(self, channel: Channel) -> None:
        """! Test start and stop methods."""
        with patch("framework.support.reports.log.logger.info") as mock_log:
            channel.start()
            channel.stop()
            assert mock_log.call_args_list == [
                call("Timer 1 started with period 1 microseconds."),
                call("Timer 1 stopped."),
            ]


class TestPITChannelManager:
    """! Test PITChannelManager class."""

    @pytest.fixture
    def pit_channel_manager(self) -> Generator[PITChannelManager, None, None]:
        """! Create a PITChannelManager."""
        channel_manager: PITChannelManager = PITChannelManager()
        yield channel_manager

    def test_create_channel_already_exists(
        self, pit_channel_manager: PITChannelManager, mocker: MagicMock
    ) -> None:
        """! Test create_channel method when channel already exists."""
        mocker.patch.dict(pit_channel_manager.channels, {1: mocker.MagicMock()})
        with patch("framework.support.reports.log.logger.error") as mock_log:
            pit_channel_manager.create_channel(1)
            mock_log.assert_called_once_with("Channel with ID 1 already exists.")

    def test_create_start_stop_channel(
        self, pit_channel_manager: PITChannelManager
    ) -> None:
        """! Test create, start and stop channel."""
        with patch("framework.support.reports.log.logger.info") as mock_log:
            pit_channel_manager.create_channel(2)
            pit_channel_manager.start_channel(2)
            pit_channel_manager.stop_channel(2)
            assert mock_log.call_args_list == [
                call("Channel with ID 2."),
                call("Timer 2 started with period 1 microseconds."),
                call("Timer 2 stopped."),
            ]

    def test_set_period_us_not_found(
        self, pit_channel_manager: PITChannelManager
    ) -> None:
        """! Test set_period_us method when channel is not found."""
        with patch("framework.support.reports.log.logger.error") as mock_log:
            pit_channel_manager.set_period_us(3, 2000)
            mock_log.assert_called_once_with("No channel found with ID 3.")

    def test_enable_interrupt(
        self, pit_channel_manager: PITChannelManager, mocker: MagicMock
    ) -> None:
        """! Test enable_interrupt method."""
        pit_channel_manager.create_channel(4)
        pit_channel_manager.enable_interrupt(4, 3000, mocker.MagicMock())
        assert pit_channel_manager.channels[4].irq_id == 3000
        assert pit_channel_manager.channels[4].irq_enable

    def test_enable_interrupt_not_found(
        self, pit_channel_manager: PITChannelManager, mocker: MagicMock
    ) -> None:
        """! Test enable_interrupt method when channel is not found."""
        with patch("framework.support.reports.log.logger.error") as mock_log:
            pit_channel_manager.enable_interrupt(5, 3000, mocker.MagicMock())
            mock_log.assert_called_once_with("No channel found with ID 5.")

    def test_disable_interrupt(self, pit_channel_manager: PITChannelManager) -> None:
        """! Test disable_interrupt method."""
        pit_channel_manager.create_channel(6)
        pit_channel_manager.disable_interrupt(6)
        assert not pit_channel_manager.channels[6].irq_enable

    def test_disable_interrupt_not_found(
        self, pit_channel_manager: PITChannelManager
    ) -> None:
        """! Test disable_interrupt method when channel is not found."""
        with patch("framework.support.reports.log.logger.error") as mock_log:
            pit_channel_manager.disable_interrupt(7)
            mock_log.assert_called_once_with("No channel found with ID 7.")
