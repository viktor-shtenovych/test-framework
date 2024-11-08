import threading
from typing import Dict, Optional

from framework.support.reports import logger
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    TInterruptCallback,
    TimerManagerABC,
)
from framework.support.vtime import VirtualTimeWorker, TimeEvent


class Timer:
    """A simple timer class that simulates hardware timer behavior with callbacks on timeouts."""

    def __init__(
        self, timer_id: int, irq_id: int, interrupt_callback: TInterruptCallback
    ):
        self.timer_id = timer_id
        self.irq_id = irq_id
        self.period_us: int = 1
        self.interrupt_callback = interrupt_callback
        self._timer_thread: Optional[threading.Thread] = None
        self._stop_event = TimeEvent()

    def start(self) -> None:
        """Start the timer."""
        if self._timer_thread is not None:
            # If timer is already running - restart it
            logger.info(f"Timer {self.timer_id} is already running, restarting.")
            self.stop()
        self._stop_event.clear()
        self._timer_thread = VirtualTimeWorker(target=self._run, daemon=True)
        self._timer_thread.start()
        logger.info(
            f"Timer {self.timer_id} started with period {self.period_us} microseconds."
        )

    def stop(self) -> None:
        """Stop the timer."""
        if self._timer_thread is None:
            # Stop API could be called multiple times in a row by the emulator
            logger.debug(f"Timer {self.timer_id} is not running.")
            return
        logger.debug(f"Timer {self.timer_id} stop called.")
        self._stop_event.set()
        self._timer_thread.join()
        self._timer_thread = None

    def _run(self) -> None:
        """Internal method to run the timer logic."""
        while True:
            if not self._stop_event.wait(self.period_us / 1_000_000.0):
                self.interrupt_callback(self.irq_id)
                logger.debug(f"Timer {self.timer_id} timeout, interrupt generated.")
            else:
                logger.info(f"Timer {self.timer_id} stopped.")
                break


class TimerManager(TimerManagerABC):
    """Manages multiple independent timers."""

    def __init__(self) -> None:
        self.timers: Dict[int, Timer] = {}
        self.lock = threading.Lock()

    def create_timer(
        self, timer_id: int, irq_id: int, callback: TInterruptCallback
    ) -> None:
        """Create a timer with a given ID and IRQ ID."""
        with self.lock:
            if timer_id in self.timers:
                logger.error(f"Timer with ID {timer_id} already exists.")
                return
            self.timers[timer_id] = Timer(timer_id, irq_id, callback)
            logger.info(f"Timer with ID {timer_id} created with IRQ ID {irq_id}.")

    def start_timer(self, timer_id: int) -> None:
        """Start a timer by its ID."""
        if timer_id not in self.timers:
            logger.error(f"No timer found with ID {timer_id}.")
            return
        self.timers[timer_id].start()

    def stop_timer(self, timer_id: int) -> None:
        """Stop a timer by its ID."""
        if timer_id not in self.timers:
            logger.error(f"No timer found with ID {timer_id}.")
            return
        self.timers[timer_id].stop()

    def set_timer_period(self, timer_id: int, period_us: int) -> None:
        """Set the period of a timer."""
        if timer_id not in self.timers:
            logger.error(f"No timer found with ID {timer_id}.")
            return
        self.timers[timer_id].period_us = period_us
        logger.debug(f"Timer {timer_id} period set to {period_us} microseconds.")

    def stop_all_timers(self) -> None:
        """Stop all running timers."""
        for timer in self.timers.values():
            timer.stop()
