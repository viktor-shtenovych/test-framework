from threading import Thread
from typing import Generator, cast

import pytest
from unittest.mock import patch, MagicMock, call

from framework.core.control.lpit import TimerManager, Timer


class TestTimer:
    """Test Timer class."""

    @pytest.fixture
    def timer(self, mocker: MagicMock) -> Generator[Timer, None, None]:
        """Create a Timer."""
        mocker.patch("threading.Thread")
        interrupt_callback: MagicMock = mocker.MagicMock()
        _timer: Timer = Timer(
            timer_id=1,
            irq_id=300,
            interrupt_callback=interrupt_callback,
        )
        yield _timer

    def test_timer_start_already_running(self, timer: Timer, mocker: MagicMock) -> None:
        """
        Test start method when timer is already running.

        Args:
            timer: Timer.
            mocker: Mocking framework.
        """
        timer._timer_thread = cast(MagicMock, mocker.MagicMock(spec=Thread))
        if timer._timer_thread is not None:
            timer._timer_thread.is_alive.return_value = True
            with patch("framework.support.reports.log.logger.info") as mock_log:
                timer.start()
                assert mock_log.call_args_list == [
                    call("Timer 1 is already running, restarting."),
                    call("Timer 1 started with period 1 microseconds."),
                ]
                timer.stop()

    def test_timer_stop_not_running(self, timer: Timer) -> None:
        """
        Test stop method when timer is not running.
        """
        with patch("framework.support.reports.log.logger.debug") as mock_log:
            timer.stop()
            mock_log.assert_called_once_with("Timer 1 is not running.")

    def test_timer_start_stop(self, timer: Timer) -> None:
        """
        Test start and stop methods.
        """
        with patch("framework.support.reports.log.logger.info") as mock_log:
            timer.start()
            timer.stop()
            assert mock_log.call_args_list == [
                call("Timer 1 started with period 1 microseconds."),
                call("Timer 1 stopped."),
            ]


class TestTimerManager:
    """
    Test TimerManager class.
    """

    @pytest.fixture
    def timer_manager(self) -> Generator[TimerManager, None, None]:
        """
        Create a TimerManager.
        """
        tm: TimerManager = TimerManager()
        yield tm

    def test_create_timer_already_exists(
        self, timer_manager: TimerManager, mocker: MagicMock
    ) -> None:
        """
        Test create_timer method when timer already exists.
        """
        mocker.patch.dict(timer_manager.timers, {1: mocker.MagicMock()})
        with patch("framework.support.reports.log.logger.error") as mock_log:
            timer_manager.create_timer(1, 1000, mocker.MagicMock())
            mock_log.assert_called_once_with("Timer with ID 1 already exists.")

    def test_create_start_stop_timer(
        self, timer_manager: TimerManager, mocker: MagicMock
    ) -> None:
        """
        Test create, start and stop timer.
        """
        callback: MagicMock = mocker.MagicMock()
        with patch("framework.support.reports.log.logger.info") as mock_log:
            timer_manager.create_timer(2, 1000, callback)
            timer_manager.start_timer(2)
            timer_manager.stop_timer(2)
            assert mock_log.call_args_list == [
                call("Timer with ID 2 created with IRQ ID 1000."),
                call("Timer 2 started with period 1 microseconds."),
                call("Timer 2 stopped."),
            ]

    def test_set_timer_period_not_found(self, timer_manager: TimerManager) -> None:
        """
        Test set_timer_period method when timer is not found.
        """
        with patch("framework.support.reports.log.logger.error") as mock_log:
            timer_manager.set_timer_period(3, 2000)
            mock_log.assert_called_once_with("No timer found with ID 3.")
