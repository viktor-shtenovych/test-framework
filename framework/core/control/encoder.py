from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    TInterruptCallback,
)
from framework.core.control.ftm_channel import FtmChannel


class Encoder:
    """
    A class that implements the Encoder driver.

    Attributes:
        min_value: The minimum value of the encoder.
        max_value: The maximum value of the encoder.
        channel: An instance of the FtmChannel class.
    """

    def __init__(self, raise_interrupt_func: TInterruptCallback) -> None:
        self.min_value = 1
        self.max_value = 3046
        self.channel = FtmChannel(
            instance=3,
            channel=4,
            irq_id=0,
            value=self.min_value,
            interrupt_callback=raise_interrupt_func,
        )
        self.channel.period_us = 3050  # PWM Freq - 328 Hz (3050 us)

    def set_value(self, value: int) -> None:
        """
        Set the value of the encoder.

        Args:
            value: The value to set.
        """
        if self.min_value <= value <= self.max_value:
            # On Anterior FSW encoder value is reversed
            self.channel.value = self.max_value - value
        else:
            raise ValueError(
                f"Encoder value shall be in <{self.min_value}: {self.max_value}>. {value} received"
            )

    def get_value(self) -> int:
        """
        Get the value of the encoder.

        Returns:
            The value of the encoder.
        """
        # On Anterior FSW encoder value is reversed
        return self.max_value - self.channel.value
