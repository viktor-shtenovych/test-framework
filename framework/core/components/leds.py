from enum import IntEnum

from framework.hardware_interfaces.drivers.common.definitions.interfaces import Pins
from framework.hardware_interfaces.drivers.common.definitions.pins_def import OutputPins
from framework.core.devices.led_driver_adp8866 import LedDriverADP8866, LedMode


class GpioLed:
    """
    A class to represent a GPIO LED.

    Attributes:
        _pins_drv (Pins): The pins driver.
        _port (int): The port.
        _pin (int): The pin.
    """

    def __init__(self, pins_drv: Pins, port: int, pin: int) -> None:
        self._pins_drv = pins_drv
        self._port = port
        self._pin = pin

    @property
    def enabled(self) -> bool:
        """
        Get the enabled status of the LED.

        Returns:
            bool: The enabled status.
        """
        return self._pins_drv.get(self._port, self._pin)


class LedDrvChannels(IntEnum):
    """
    An enumeration to represent the LED driver channels.
    """

    LEFT_YELLOW_1 = 1
    LEFT_YELLOW_2 = 2
    LEFT_YELLOW_3 = 3
    LEFT_YELLOW_4 = 4
    RIGHT_YELLOW = 5
    RIGHT_GREEN = 6
    RIGHT_BLUE = 7
    RIGHT_RED = 8
    SYSTEM_LED = 16


class Leds:
    """
    A class to represent the LEDs.

    Attributes:
        _system_led (GpioLed): The system LED.
        _led_driver (LedDriverADP8866): The LED driver.
    """

    def __init__(self, pins_drv: Pins, led_driver: LedDriverADP8866) -> None:
        self._system_led = GpioLed(pins_drv, *OutputPins.LED_SYSTEM.value)
        self._led_driver = led_driver

    @property
    def LED_MODE(self) -> type[LedMode]:
        """
        Get the LED mode.

        Returns:
            type[LedMode]: The LED mode.
        """
        return LedMode

    @property
    def LEDS(self) -> type[LedDrvChannels]:
        """
        Get the LED driver channels.

        Returns:
            type[LedDrvChannels]: The LED driver channels.
        """
        return LedDrvChannels

    def get_led_mode(self, led: LedDrvChannels) -> LedMode:
        """
        Get the LED mode.

        Args:
            led (LedDrvChannels): The LED driver channel.

        Returns:
            LedMode: The LED mode.
        """
        if led == LedDrvChannels.SYSTEM_LED:
            return LedMode.OFF if self._system_led.enabled else LedMode.ON_SOLID
        else:
            return self._led_driver.get_led_mode(led.value)
