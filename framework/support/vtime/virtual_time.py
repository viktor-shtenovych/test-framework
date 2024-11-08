import threading
from typing import List

from framework.support.reports import logger
from framework.support.vtime.workers import get_worker_manager, VirtualTimeWorker


class TimeOutEvent(threading.Event):
    """Event with set timeout used for calculation of next clock step/value. The event is set.

    - by VirtualTimeManager when (virtual) timeout is reached;
    - when `TimeEvent` waiting for this TimeoutEvent is set.

    This class is supposed to be used only within this module.
    """

    def __init__(self, wake_up_time: int | None) -> None:
        super().__init__()
        self._wake_up_time = wake_up_time
        self._expired = False
        self.worker_id = VirtualTimeWorker.current_worker()

    @property
    def wake_up_time(self) -> int | None:
        """
        Property that returns the wake-up time of the TimeoutEvent.

        Returns:
            The wake-up time of the TimeoutEvent. The return type can be int or None.
        """
        return self._wake_up_time

    def expire(self) -> None:
        """
        Marks the TimeoutEvent as expired and sets the event.

        This method also activates the worker associated with this TimeoutEvent.
        """
        self._expired = True
        self.set()
        get_worker_manager().go_active(self.worker_id)

    @property
    def expired(self) -> bool:
        """
        Marks the TimeoutEvent as expired and sets the event.

        This method also activates the worker associated with this TimeoutEvent.
        """
        return self._expired

    def wait(self, timeout: float | None = None) -> bool:
        """Puts the worker associated with this TimeoutEvent into an idle state.

         Waits for the event to be set or for the timeout to expire, and then activates the worker again.

        Args:
            timeout: The maximum time to wait for the event to be set. If None, waits indefinitely.

        Returns:
            True if the event was set before the timeout expired, False otherwise.
        """
        get_worker_manager().go_idle(self.worker_id)
        result = super().wait(timeout)
        get_worker_manager().go_active(self.worker_id)
        return result

    def set(self) -> None:
        """
        Activates the worker associated with this TimeoutEvent and sets the event.

        This method is typically used to wake up any threads that are waiting for this event.
        """
        get_worker_manager().go_active(self.worker_id)
        super().set()


class VirtualTimeManager:
    """Virtual vtime manager.

    Is responsible for handling virtual vtime simulating system clock of real device where
    this clock 'ticks' every millisecond.

    For simulation purposes we need to ensure:
    - Clock does not 'tick' when simulator is not ready (to prevent timeouts in footswitch sw) or emulator is
    not ready (to prevent timeouts in simulator). This is ensured by waiting for emulator and simulator (this framework)
    to be in idle state. In simulator all workers (thread) have to be waiting for an event (which has a timeout set).
    - Clock is increased as much as possible (doest not need to be 1). This is ensured by knowing timeout
    of each worker(thread). The step is `min(timeouts of all workers)`.

    This VirtualTimeManager implementation uses list of `TimeOutEvent` objects. Each `TimeOutEvent` (if not set)
    represents an idle worker and has timeout property.

    Method `_idle_reached` is called from `WorkersManager` when all threads (which are expected to be affected
    by virtual vtime) are in idle state.
    """

    def __init__(self) -> None:
        self._clock_us = 0
        self._time_events: List[TimeOutEvent] = []
        get_worker_manager().register_idle_observer(self._idle_reached)
        self._events_lock = threading.Lock()

    def _idle_reached(self) -> None:
        """
        Handles the situation when the emulator is in an IDLE state awaiting interrupts.

        This method is called when all threads are in an idle state. It updates the list of TimeOutEvents,
        calculates the minimum wake-up time from all wake-up times in the waiting TimeEvents, and updates the clock.
        It also updates all TimeEvents for which the wake-up time is reached and cancels the event.

        This method is part of the internal workings of the VirtualTimeManager and is not intended to be used directly.
        """
        # Step is minimum from all wake-up vtime in waiting TimeEvents and `max_step_ms` argument
        with self._events_lock:
            self._time_events = [
                event for event in self._time_events if not event.is_set()
            ]
        if self._time_events:
            wakeup_times = [
                event.wake_up_time
                for event in self._time_events
                if event.wake_up_time is not None
            ]
            if any(wakeup_times):
                self._clock_us = min(wakeup_times)

                # Update all TimeEvents for which wake-up vtime is reached
                for event in set(self._time_events):
                    if event.wake_up_time == self._clock_us:
                        event.expire()
                        self.cancel_event(event)

    def get_timeout_event(self, timeout_s: float | None) -> TimeOutEvent:
        """Creates and returns a TimeOutEvent object.

        This object is included in list of timeouts used for calculation
        of next clock step.
        """
        wake_up_time = int(self._clock_us + (timeout_s * 1e6)) if timeout_s else None
        timeout = TimeOutEvent(wake_up_time=wake_up_time)
        with self._events_lock:
            self._time_events.append(timeout)
        return timeout

    def cancel_event(self, event: TimeOutEvent) -> None:
        """Cancel timeout event (e.g. when awaiting data and data were generated by different worker)."""
        try:
            with self._events_lock:
                self._time_events.remove(event)
        except ValueError:
            pass

    def timeout_all_events(self) -> None:
        """Raise timeout for all events to allow all workers to continue (e.g. when cleaning up)."""
        for event in self._time_events:
            event.expire()

    def sleep(self, secs: float) -> None:
        """Sleep for defined virtual milliseconds."""
        event = self.get_timeout_event(secs)
        event.wait()

    def time_ms(self) -> int:
        """Current value of virtual vtime."""
        return int(self._clock_us * 1e-3)

    def time_us(self) -> int:
        """Current value of virtual vtime in microseconds."""
        return self._clock_us

    def reset(self) -> None:
        """Reset virtual time."""
        self._clock_us = 0
        if get_worker_manager().get_num_of_workers() > 0:
            logger.error("Workers still active when resting virtual time")


class TimeEvent(threading.Event):
    """Event implementation affecting virtual vtime. Worker is considered idle when waiting for this event."""

    def __init__(self) -> None:
        super().__init__()
        self._waiters: List[TimeOutEvent] = []

    def set(self) -> None:
        """
        Sets the event and cancels the associated timeout events.

        This method iterates over all timeout events associated with this TimeEvent,
        cancels them in the VirtualTimeManager, and sets them.
        After all timeout events are processed, it sets this TimeEvent.

        Note: There is no need to clear the waiters list as all elements are removed by the wait itself.
        """
        for timeout in self._waiters:
            vtime_manager.cancel_event(timeout)
            timeout.set()
        super().set()

    def wait(self, timeout: float | None = None) -> bool:
        """Wait for event until it is set or timeout is reached. During wait worker is in idle state."""
        if self.is_set():
            return True

        timeout_event = vtime_manager.get_timeout_event(timeout)
        self._waiters.append(timeout_event)
        timeout_event.wait()
        if timeout_event in self._waiters:
            self._waiters.remove(timeout_event)
        return not timeout_event.expired


vtime_manager = VirtualTimeManager()
