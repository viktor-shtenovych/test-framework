import struct

from framework.support.reports import logger
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    FtmChannelABC,
    TInterruptCallback,
)
from framework.core.control.lpit import Timer


class FtmChannel(Timer, FtmChannelABC):
    """
    A class to represent a FlexTimer channel.
    """

    def __init__(
        self,
        instance: int,
        channel: int,
        irq_id: int,
        value: int,
        interrupt_callback: TInterruptCallback,
    ):
        # Timer ID for internal use have an offset 16
        super().__init__(channel + 16, irq_id, interrupt_callback)
        self.instance = instance
        self.channel = channel
        self.value = value
        self.period_us = 10_000

    def _run(self) -> None:
        """Internal method to run the timer logic."""
        while True:
            if not self._stop_event.wait(self.period_us / 1_000_000.0):
                flags = int.from_bytes(
                    struct.pack(">BBH", self.instance, self.channel, self.value),
                    byteorder="big",
                )
                self.interrupt_callback(self.irq_id, flags)
                logger.debug(
                    f"FTM CH {self.channel} timeout, interrupt flags: {flags}."
                )
            else:
                logger.info(f"FTM CH {self.channel} stopped.")
                break
