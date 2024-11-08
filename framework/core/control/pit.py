"""! @brief Defines simple timer that simulates hardware timer behavior."""
##
# @file pit.py
#
# @brief Defines simple timer that simulates hardware timer behavior.
#
# @section description_pit Description
# This module represents the Channel and the PITChannelManager classes.
#
# @section libraries_pit Libraries/Modules
# - threading standard library (https://docs.python.org/uk/3/library/threading.html)
# - typing standard library (https://docs.python.org/3/library/typing.html)
# - interfaces module (local)
#   - Access to PITChannelManagerABC class.
#   - Access to TInterruptCallback class.
# - vtime module (local)
#   - Access to VirtualTimeWorker class.
#   - Access to TimeEvent class.
#
# @section notes_pit Notes
# - None.
#
# @section todo_pit TODO
# - None.
#
# @section author_pit Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 09/09/2024.
# - Modified by:
#   - Maksym Masalov maksym.masalov@globallogic.com on 12/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.

import threading
from typing import Dict

from framework.hardware_interfaces.drivers.common.definitions.channel import Channel
from framework.support.reports import logger
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    TInterruptCallback,
    PITChannelManagerABC,
)


class PITChannelManager(PITChannelManagerABC):
    """! Manages multiple independent timers."""

    def __init__(self) -> None:
        self.channels: Dict[int, Channel] = {}
        self.lock = threading.Lock()

    def create_channel(self, channel_id: int) -> None:
        """! Create a channel with a given ID."""
        with self.lock:
            if channel_id in self.channels:
                logger.error(f"Channel with ID {channel_id} already exists.")
                return
            self.channels[channel_id] = Channel(channel_id)
            logger.info(f"Channel with ID {channel_id}.")

    def start_channel(self, channel_id: int) -> None:
        """! Start a channel by its ID."""
        if channel_id not in self.channels:
            logger.error(f"No channel found with ID {channel_id}.")
            return
        self.channels[channel_id].start()

    def stop_channel(self, channel_id: int) -> None:
        """! Stop a channel by its ID."""
        if channel_id not in self.channels:
            logger.error(f"No channel found with ID {channel_id}.")
            return
        self.channels[channel_id].stop()

    def set_period_us(self, channel_id: int, period_us: int) -> None:
        """! Set the period of a channel."""
        if channel_id not in self.channels:
            logger.error(f"No channel found with ID {channel_id}.")
            return
        self.channels[channel_id].period_us = period_us
        logger.debug(f"Channel {channel_id} period set to {period_us} microseconds.")

    def enable_interrupt(
        self, channel_id: int, irq_id: int, callback: TInterruptCallback
    ) -> None:
        """! Enable timer's interrupt."""
        if channel_id not in self.channels:
            logger.error(f"No channel found with ID {channel_id}.")
            return
        self.channels[channel_id].irq_id = irq_id
        self.channels[channel_id].interrupt_callback = callback
        self.channels[channel_id].irq_enable = True

    def disable_interrupt(self, channel_id: int) -> None:
        """! Disable timer's interrupt."""
        if channel_id not in self.channels:
            logger.error(f"No channel found with ID {channel_id}.")
            return
        self.channels[channel_id].irq_enable = False

    def stop_all(self) -> None:
        """! Stop all running channels."""
        for timer in self.channels.values():
            timer.stop()
