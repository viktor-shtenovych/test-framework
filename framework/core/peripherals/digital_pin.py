from typing import Callable, List

from framework.hardware_interfaces.drivers.common.definitions.interfaces import Pins
from framework.support.reports import logger


class DigitalOutput:
    """
    ! GPIO output from app.
    """

    def __init__(self, pins_drv: Pins, port: int, pin: int) -> None:
        self.pins_drv = pins_drv
        self.port = port
        self.pin = pin
        self._state_change_subscribers: List[Callable[[bool], None]] = []

    @property
    def state(self) -> bool:
        """
        ! Get the state of the digital output.

        @return The state of the digital output.
        """
        try:
            return self.pins_drv.get(self.port, self.pin)
        except TypeError:
            return self.pins_drv.get(self.pin)

    @state.setter
    def state(self, value: bool) -> None:
        """
        ! Set the state of the digital output.

        @param value The state to set the digital output to.
        """
        old_state = self.state
        try:
            self.pins_drv.set(self.port, self.pin, value)
        except TypeError:
            self.pins_drv.set(self.pin, value)
        if old_state != value:
            for callback in self._state_change_subscribers:
                callback(value)

    def subscribe_on_state_change(self, callback: Callable[[bool], None]) -> None:
        """
        ! Subscribe to state change events.

        @param callback The callback to call when the state changes.
        """
        self._state_change_subscribers.append(callback)


class DigitalInput:
    """
    ! GPIO input to app.
    """

    def __init__(
        self, pins_drv: Pins, port: int, pin: int, active_low: bool = False
    ) -> None:
        self.pins_drv = pins_drv
        self.port = port
        self.pin = pin
        self.active_low = active_low

    @property
    def state(self) -> bool:
        """
        ! Get the state of the digital input.

        @return The state of the digital input.
        """
        try:
            return self.pins_drv.get(self.port, self.pin) != self.active_low
        except TypeError:
            return self.pins_drv.get(self.pin) != self.active_low

    @state.setter
    def state(self, value: bool) -> None:
        """
        ! Set the state of the digital input.

        @param value The state to set the digital input to.
        """
        _value_to_set = value != self.active_low
        logger.debug(f"Setting pin {self.port}/{self.pin} to {_value_to_set}")
        try:
            self.pins_drv.set(self.port, self.pin, _value_to_set)
        except TypeError:
            self.pins_drv.set(self.pin, _value_to_set)
