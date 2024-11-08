import threading
from typing import Optional, Callable

from framework.support.reports import logger

from framework.support.vtime import VirtualTimeWorker, TimeEvent


class RTC_Timer:
    """A simple timer class that simulates RTC behavior with interrupts every second."""

    def __init__(self, irq_id: int, raise_interrupt_func: Callable[[int, int], None]):
        with threading.Lock():
            self.irq_id = irq_id
            self._timer_thread: Optional[threading.Thread] = None
            self._stop_event = TimeEvent()
            self._raise_interrupt = raise_interrupt_func

            self._time_seconds: int = 1704067200  # 00:00:00 UTC on 1 January 2024

    def _add_second(self) -> None:
        """Increment the time by one second."""
        self._time_seconds += 1

    def set_seconds(self, seconds: int) -> None:
        """
        Set the time in seconds.

        Args:
            seconds: The time in seconds.
        """
        self._time_seconds = seconds

    def _get_seconds(self) -> int:
        """
        Get the current time in seconds.

        Returns:
            The current time in seconds.
        """
        return self._time_seconds

    def start(self) -> None:
        """Start the clock."""
        if self._timer_thread is not None:
            # If timer is already running - restart it
            logger.info("RTC is already running, restarting.")
            self.stop()
        self._stop_event.clear()
        self._timer_thread = VirtualTimeWorker(target=self._run, daemon=True)
        self._timer_thread.start()
        logger.info("RTC started.")

    def stop(self) -> None:
        """Stop the clock."""
        if self._timer_thread is None:
            # Stop API could be called multiple times in a row by the emulator
            logger.debug("RTC is not running.")
            return
        logger.debug("RTC stop called.")
        self._stop_event.set()
        self._timer_thread.join()
        self._timer_thread = None

    def _run(self) -> None:
        """
        Run the timer.

        This method is called in a separate thread.
        """
        while True:
            if not self._stop_event.wait(1):
                self._add_second()
                self._raise_interrupt(self.irq_id, self._get_seconds())
                logger.debug("RTC timeout, interrupt generated.")
            else:
                logger.info("RTC stopped.")
                break
