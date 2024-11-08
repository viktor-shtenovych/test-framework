import dataclasses
import struct
from typing import Any, Dict, Callable

import bitstruct

from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    BasePinDriver,
)
from framework.support.reports import logger, rpc_call
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.hardware_interfaces.protoc.s32k148.s32k148_pins_driver_pb2 import (
    PinsInitParams,
    PinSetDirectionParams,
    PinWriteParams,
    Direction,
)
from framework.hardware_interfaces.protoc.s32k148.s32k148_pins_driver_pb2_grpc import (
    PinsDriverServicer,
)
from framework.support.vtime import TimeEvent


@dataclasses.dataclass(frozen=True)
class PinPort:
    """
    Dataclass to represent a GPIO pin port.

    Attributes:
        port (int): The port.
        pin (int): The pin.
    """

    port: int
    pin: int


@dataclasses.dataclass
class PinPortData:
    """
    Dataclass to represent a GPIO pin port data.

    Attributes:
        direction (Direction): The direction.
        value (int): The value.
    """

    direction: Direction
    value: int


class PinDriver(PinsDriverServicer, BasePinDriver):
    """Stub for GPIO pins."""

    def __init__(self, raise_interrupt_func: Callable[[int, int], None]) -> None:
        super().__init__()
        self.port_pins: Dict[PinPort, PinPortData] = {}
        self.interrupts: Dict[int, int] = {}
        self._ready = TimeEvent()
        self._raise_interrupt = raise_interrupt_func

    def set(self, port: int, pin: int, value: bool) -> None:
        """
        Set the value of a pin.

        Args:
            port (int): The port.
            pin (int): The pin.
            value (bool): The value.
        """
        self.port_pins[PinPort(port, pin)].value = value
        pin_values = []
        for i in range(32):
            pin_port = PinPort(port, i)
            pin_values.append(
                self.port_pins[pin_port].value if pin_port in self.port_pins else 0
            )

        flags = struct.unpack(">I", bitstruct.pack(32 * "b1", *reversed(pin_values)))[0]
        self._raise_interrupt(self.interrupts[port], flags)

    def get(self, port: int, pin: int) -> bool:
        """
        Get the value of a pin.

        Args:
            port (int): The port.
            pin (int): The pin.

        Returns:
            bool: The value.
        """
        pin_port = PinPort(port, pin)
        if pin_port not in self.port_pins:
            raise KeyError(f"{pin_port} not configured/initialized")
        return bool(self.port_pins[pin_port].value)

    def wait_for_initialization(self) -> None:
        """
        Wait for the initialization.

        This method is used to wait for the initialization of the driver.
        """
        logger.debug(f"Wait for {self.__class__.__name__} initialization")
        self._ready.wait()
        logger.info(f"{self.__class__.__name__} initialized")

    # PinsDrv methods

    @rpc_call
    def PINS_DRV_Init(self, request: PinsInitParams, context: Any) -> Status:
        """
        Initialize the pins.
        """
        self.port_pins = {
            PinPort(item.port_id, item.pin_id): PinPortData(
                item.direction, item.init_value
            )
            for item in request.config
        }
        self.interrupts = {
            setting.port_id: setting.irq_id for setting in request.irq_ids
        }
        self._ready.set()
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def PINS_DRV_SetDirection(
        self, request: PinSetDirectionParams, context: Any
    ) -> Status:
        """
        Set the direction of a pin.
        """
        self.port_pins[
            PinPort(request.port_id, request.pin_id)
        ].direction = request.direction
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def PINS_DRV_WritePin(self, request: PinWriteParams, context: Any) -> Status:
        """
        Write to a pin.
        """
        self.port_pins[PinPort(request.port_id, request.pin_id)].value = request.value
        return Status(status=StatusEnum.STATUS_SUCCESS)
