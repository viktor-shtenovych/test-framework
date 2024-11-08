from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    PwmChannelABC,
)


class Pwm(PwmChannelABC):
    """
    A class to represent a PWM channel.
    """

    def get_duty_cycle(self) -> int:
        """
        Get the duty cycle of the PWM channel.

        Returns:
            int: The duty cycle of the PWM channel.
        """
        return self.duty_cycle
