import time
from threading import Thread
from typing import Iterator

import pytest
from framework.core.control.lpit import TimerManager
from framework.hardware_interfaces.drivers.common.interrupts import Interrupts
from framework.support.vtime import vtime_manager


@pytest.fixture(scope="module")
def timer_manager() -> Iterator[TimerManager]:
    """
    Fixture to create a TimerManager instance.
    """
    yield TimerManager()


@pytest.fixture(scope="function")
def irq_mgr() -> Iterator[Interrupts]:
    """
    Fixture to create an Interrupts instance.
    """
    irq_mgr = Interrupts()
    irq_mgr.start()
    yield irq_mgr
    irq_mgr.stop()


def test_single_timer_lifecycle(
    timer_manager: TimerManager, irq_mgr: Interrupts
) -> None:
    """
    Test single timer lifecycle.
    """
    timer_id = 4
    irq_id = 3004
    period_us = 1_000_000  # 1 second

    # Create and start timer"
    start_time = vtime_manager.time_ms()
    timer_manager.create_timer(timer_id, irq_id, irq_mgr.raise_interrupt)
    timer_manager.set_timer_period(timer_id, period_us)
    timer_manager.start_timer(timer_id)
    time.sleep(0.1)

    # Check interrupts and virtual vtime
    for iteration in range(1, 3):
        assert irq_id == irq_mgr.wait_for_interrupt().irq_id
        expected = start_time + iteration * (period_us * 1e-3)
        assert expected == vtime_manager.time_ms()
    timer_manager.stop_timer(timer_id)
    vtime_manager.timeout_all_events()


def test_multiple_timers_concurrent(
    timer_manager: TimerManager, irq_mgr: Interrupts
) -> None:
    """
    Test multiple timers running concurrently.
    """
    timers = [
        (1, 3001, 500_000),  # Timer ID 1, IRQ ID 3001, period 0.5 seconds
        (2, 3002, 750_000),  # Timer ID 2, IRQ ID 3002, period 0.75 seconds
        (3, 3003, 1_000_000),  # Timer ID 3, IRQ ID 3003, period 1 second
    ]
    next_expected_interrupt = {}
    periods = {timer[1]: timer[2] for timer in timers}
    counters = {timer[1]: 0 for timer in timers}

    def setup_and_run_timer(timer_id: int, irq_id: int, period_us: int) -> None:
        # Create and start timer with ID{timer_id}, irq_id{irq_id} and period {period_us}
        timer_manager.create_timer(timer_id, irq_id, irq_mgr.raise_interrupt)
        timer_manager.set_timer_period(timer_id, period_us)
        timer_manager.start_timer(timer_id)

    # Start multiple timers threads
    threads = []
    for timer_id, irq_id, period_us in timers:
        thread = Thread(target=setup_and_run_timer, args=(timer_id, irq_id, period_us))
        threads.append(thread)
        thread.start()

    time.sleep(0.1)  # Give all timer vtime to start

    # Check interrupts and virtual vtime
    interrupt = 0
    for iteration in range(1, 30):
        interrupt = irq_mgr.wait_for_interrupt().irq_id
        current_vtime = vtime_manager.time_us()
        if interrupt not in next_expected_interrupt:
            next_expected_interrupt[interrupt] = current_vtime
        expected_vtime = next_expected_interrupt[interrupt]
        counters[interrupt] += 1
        assert expected_vtime == current_vtime
        next_expected_interrupt[interrupt] += periods[interrupt]

    assert all(counter > 1 for counter in counters.values())
    next_expected_interrupt[interrupt] += periods[interrupt]

    for timer in timer_manager.timers:
        timer_manager.stop_timer(timer)

    time.sleep(0.1)  # Wait for all timers to get the stop event
    vtime_manager.timeout_all_events()

    for thread in threads:
        thread.join()
