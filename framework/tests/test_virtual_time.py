"""Virtual vtime manager unit tests."""

import concurrent.futures
import threading
import time
from concurrent.futures import ALL_COMPLETED
from queue import Empty


from framework.support.reports import logger
from framework.support.vtime.queue import Queue
from framework.support.vtime import VirtualTimeManager, vtime_manager, TimeEvent
from framework.support.vtime import (
    VirtualTimeThreadPoolExecutor,
    VirtualTimeWorker,
)


def _sleep(vm: VirtualTimeManager, duration: int) -> None:
    """Sleep for `duration` virtual milliseconds."""
    logger.info(f"{threading.current_thread().name} sleeping for {duration}")
    vm.sleep(duration)
    logger.info(f"{threading.current_thread().name} sleeping done")


def _event_provider(data_available: TimeEvent, delay: float) -> int:
    """
    Set the event after `delay` virtual milliseconds.

    Args:
        data_available: An event to set.
        delay: The delay in virtual milliseconds.

    Returns:
        The current virtual time.
    """
    time.sleep(0.1)
    vtime_manager.sleep(delay)
    logger.info(f"Setting event (delay: {delay})")
    data_available.set()
    return vtime_manager.time_ms()


def _event_consumer(data_available: TimeEvent, timeout: float) -> bool:
    """
    Wait for the event for `timeout` virtual milliseconds.

    Args:
        data_available: An event to wait for.
        timeout: The timeout in virtual milliseconds.

    Returns:
        True if the event was set, False otherwise.
    """
    time.sleep(0.2)
    timeout_raised = not data_available.wait(timeout=timeout)
    logger.info(f"Event consumer finished with timeout({timeout}): {timeout_raised}")
    return timeout_raised


def _data_provider(data_queue: Queue[str]) -> None:
    """
    Produce data and sleep.

    Args:
        data_queue: A queue to put data in.
    """
    time.sleep(0.1)  # Wait for consumer to be running
    logger.info("Producer sleep")
    vtime_manager.sleep(0.05)
    logger.info("Producer data")
    data_queue.put_nowait("data")
    logger.info("Produced")
    vtime_manager.sleep(1)
    logger.info("Producer done")


def _data_consumer(data_queue: Queue[str]) -> bool:
    """
    Consume data and sleep.

    Args:
        data_queue: A queue to get data from.

    Returns:
        True if data was retrieved, False otherwise.
    """
    logger.info("Consumer sleep")
    time.sleep(
        0.2
    )  # Wait for data provider to be already running and sleeping otherwise data retrieval can vtime out
    try:
        logger.info("Consumer wait for data")
        data_queue.get(timeout=0.1)
        logger.info("Consumer done")
        data_retrieved = True
    except Empty:
        logger.info("Consumer empty")
        data_retrieved = False
    vtime_manager.sleep(1)
    return data_retrieved


def test_time_increments() -> None:
    """
    Test the time increments.

    The time should increment by 1 every second.
    """
    logger.info("Test case starting")
    data_available = TimeEvent()
    start_time = vtime_manager.time_ms()

    provider = VirtualTimeWorker(target=lambda: _event_provider(data_available, 0.003))
    consumer1 = VirtualTimeWorker(target=lambda: _event_consumer(data_available, 0.002))
    consumer2 = VirtualTimeWorker(target=lambda: _event_consumer(data_available, 0.01))

    provider.start()
    consumer1.start()
    consumer2.start()

    provider.join()
    consumer1.join()
    consumer2.join()

    assert vtime_manager.time_ms() == start_time + 3


def test_pool_executor() -> None:
    """
    Test the virtual time pool executor.
    """
    with VirtualTimeThreadPoolExecutor(max_workers=10) as executor:
        logger.info("Test case starting")
        data_available_pool = TimeEvent()

        start_time = vtime_manager.time_ms()

        provider = executor.submit(lambda: _event_provider(data_available_pool, 0.002))
        consumer1 = executor.submit(lambda: _event_consumer(data_available_pool, 0.001))
        consumer2 = executor.submit(lambda: _event_consumer(data_available_pool, 0.003))

        concurrent.futures.wait(
            [provider, consumer1, consumer2],  # type: ignore
            return_when=ALL_COMPLETED,
        )

        assert provider.done() and provider.exception() is None
        assert consumer1.done() and consumer1.exception() is None
        assert consumer2.done() and consumer2.exception() is None

        assert provider.result() == start_time + 2
        assert consumer1.result() is True
        assert consumer2.result() is False
        assert vtime_manager.time_ms() == provider.result()


def test_queue() -> None:
    """
    Test the virtual time queue.
    """
    with VirtualTimeThreadPoolExecutor(max_workers=10) as executor:
        logger.info("Test case starting")

        data_queue: Queue[str] = Queue()

        fut_provider = executor.submit(lambda: _data_provider(data_queue))
        fut_consumer = executor.submit(lambda: _data_consumer(data_queue))

        concurrent.futures.wait([fut_provider, fut_consumer], return_when=ALL_COMPLETED)  # type: ignore
        assert fut_consumer.result()
