"""! @Brief Manages multiple independent timers."""

#
# @file emios_channel_manager.py
#
# @section description_emios_channel_manager Description
# This module represents the EMIOS channel manager.
#
# @section libraries_emios_channel_manager Libraries/Modules
# - threading standard library (https://docs.python.org/3/library/threading.html)
# - typing standard library (https://docs.python.org/3/library/typing.html)
# - vtime module (local)
# - reports module (local)
#
# @section notes_emios_channel_manager Notes
# - None.
#
# @section todo_emios_channel_manager TODO
# - None.
#
# @section author_emios_channel_manager Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 21/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved
import threading
from typing import Dict, Tuple

from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    TInterruptCallback,
)
from framework.hardware_interfaces.drivers.common.definitions.channel import Channel
from framework.support.reports import logger


class EMIOSChannelManager:
    """! Manages multiple independent timers."""

    def __init__(self) -> None:
        self.channels: Dict[Tuple[int, int], Channel] = {}
        self.lock = threading.Lock()

    def create_channel(self, group_id: int, channel_id: int) -> None:
        """! Create a channel with a given ID."""
        with self.lock:
            if (group_id, channel_id) in self.channels:
                logger.error(f"Channel with ID {channel_id} already exists.")
                return
            self.channels[(group_id, channel_id)] = Channel(channel_id, group_id)
            logger.debug(f"Channel with ID {channel_id}.")

    def start_channel(self, group_id: int, channel_id: int) -> None:
        """! Start a channel by its ID."""
        if (group_id, channel_id) not in self.channels:
            logger.error(f"No channel found with ID {channel_id}.")
            return
        self.channels[(group_id, channel_id)].start()

    def stop_channel(self, group_id: int, channel_id: int) -> None:
        """! Stop a channel by its ID."""
        if (group_id, channel_id) not in self.channels:
            logger.error(f"No channel found with ID {channel_id}.")
            return
        self.channels[
            (
                group_id,
                channel_id,
            )
        ].stop()

    def set_period_us(self, group_id: int, channel_id: int, period_us: int) -> None:
        """! Set the period of a channel."""
        if (group_id, channel_id) not in self.channels:
            logger.error(f"No channel found with ID {channel_id}.")
            return
        with self.lock:
            channel = self.channels[(group_id, channel_id)]
            if channel.is_running():
                channel.period_us = period_us
                self.start_channel(group_id, channel_id)
            else:
                channel.period_us = period_us
        logger.debug(f"Channel {channel_id} period set to {period_us} microseconds.")

    def enable_interrupt(
        self,
        group_id: int,
        channel_id: int,
        irq_id: int,
        callback: TInterruptCallback | None,
    ) -> None:
        """! Enable timer's interrupt."""
        if (group_id, channel_id) not in self.channels:
            logger.error(f"No channel found with ID {channel_id}.")
            return
        self.channels[(group_id, channel_id)].irq_id = irq_id
        self.channels[(group_id, channel_id)].interrupt_callback = callback
        self.channels[(group_id, channel_id)].irq_enable = True

    def disable_interrupt(self, group_id: int, channel_id: int) -> None:
        """! Disable timer's interrupt."""
        if (
            group_id,
            channel_id,
        ) not in self.channels:
            logger.error(f"No channel found with ID {channel_id}.")
            return
        self.channels[
            (
                group_id,
                channel_id,
            )
        ].irq_enable = False

    def stop_all(self) -> None:
        """! Stop all running channels."""
        for timer in self.channels.values():
            timer.stop()
