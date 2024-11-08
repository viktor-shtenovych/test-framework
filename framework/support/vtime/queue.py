from queue import Queue as BaseQueue, Empty
from threading import Lock
from typing import TypeVar

from framework.support.reports import logger
from framework.support.vtime.virtual_time import TimeEvent


_T = TypeVar("_T")


class Queue(BaseQueue[_T]):
    """Queue with virtual vtime support i.e. waiting for data in empty queue leads to idle worker state."""

    def __init__(self, maxsize: int = 0) -> None:
        super().__init__(maxsize=maxsize)
        self.q_event = TimeEvent()
        self._read_lock = Lock()

    def put(self, item: _T, block: bool = True, timeout: float | None = None) -> None:
        """
        Put an item into the queue.

        Args:
            item: Item to put into the queue.
            block: If True, block until the item is inserted.
            timeout: If block is True, timeout in seconds to wait for the item to be inserted.
        """
        if block is True:
            super().put(item, block, timeout=timeout)
            self.q_event.set()
        else:
            super().put(item, block, timeout)

    def put_nowait(self, item: _T) -> None:
        """
        Put an item into the queue without blocking.

        Args:
            item: Item to put into the queue.
        """
        super().put_nowait(item)
        self.q_event.set()

    def get(self, block: bool = True, timeout: float | None = None) -> _T:
        """
        Remove and return an item from the queue.

        Args:
            block: If True, block until an item is available.
            timeout: If block is True, timeout in seconds to wait for the item to be available.
        """
        if block:
            with self._read_lock:
                if self.empty():
                    self.q_event.clear()
                if self.q_event.wait(timeout) is False:
                    logger.debug(f"Data retrieval from queue timeout ({timeout})")
                    raise Empty()
                val = super().get_nowait()
                return val
        return super().get(block=block, timeout=timeout)
