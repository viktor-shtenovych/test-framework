"""! @Brief: This snippet defines the Channel class that simulates hardware timer behavior with callbacks on timeouts."""

#
# @file channel.py
#
# @section description_channel Description
#
# This module represents the Channel class that simulates hardware timer behavior with callbacks on timeouts.
#
# @section libraries_channel Libraries/Modules
# - threading standard library (https://docs.python.org/3/library/threading.html)
#
# @section notes_channel Notes
# - None.
#
# @section todo_channel TODO
# - None.
#
# @section author_channel Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 23/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved
import threading
from typing import Optional

from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    TInterruptCallback,
)
from framework.support.reports import logger
from framework.support.vtime import VirtualTimeWorker, TimeEvent


class Channel:
    """! A simple timer class that simulates hardware timer behavior with callbacks on timeouts."""

    def __init__(self, channel_id: int, group_id: int = 0):
        self.channel_id = channel_id
        self.group_id: int = group_id
        self.irq_id: int = 0
        self.irq_enable: bool = False
        self.period_us: int = 1
        self.interrupt_callback: Optional[TInterruptCallback] = None
        self._timer_thread: Optional[threading.Thread] = None
        self._stop_event = TimeEvent()

    def start(self) -> None:
        """! Start the timer."""
        if self._timer_thread is not None:
            logger.info(f"Timer {self.channel_id} is already running, restarting.")
            self.stop()
        self._stop_event.clear()
        self._timer_thread = VirtualTimeWorker(target=self._run, daemon=True)
        self._timer_thread.start()
        logger.info(
            f"Timer {self.channel_id} started with period {self.period_us} microseconds."
        )

    def stop(self) -> None:
        """! Stop the timer."""
        if self._timer_thread is None:
            # Stop API could be called multiple times in a row by the emulator
            logger.debug(f"Timer {self.channel_id} is not running.")
            return
        logger.debug(f"Timer {self.channel_id} stop called.")
        self._stop_event.set()
        self._timer_thread.join()
        self._timer_thread = None

    def is_running(self) -> bool:
        """! Check if the timer is running."""
        return self._timer_thread is not None and self._timer_thread.is_alive()

    def _run(self) -> None:
        """! Internal method to run the timer logic."""
        while True:
            if not self._stop_event.wait(self.period_us / 1_000_000.0):
                if self.irq_enable and self.interrupt_callback is not None:
                    self.interrupt_callback(self.irq_id)
                    logger.debug(
                        f"Timer {self.channel_id} timeout, interrupt generated."
                    )
                else:
                    logger.debug(
                        f"Timer {self.channel_id} timeout, interrupt not generated (disabled)."
                    )
            else:
                logger.info(f"Timer {self.channel_id} stopped.")
                break
