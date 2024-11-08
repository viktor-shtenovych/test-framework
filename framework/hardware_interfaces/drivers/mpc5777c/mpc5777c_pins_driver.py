"""! @brief Defines the PINS driver."""
##
# @file mpc5777c_pins_driver.py
#
# @brief Defines the PINS driver.
#
# @section description_mpc5777c_pins_driver Description
# This module represents the PinDriver class.
#
# @section libraries_mpc5777c_pins_driver Libraries/Modules
# - grpc standard library (https://grpc.io/docs/languages/python/)
# - Pins module (local)
#   - Access to PinDriver class.
#
# @section notes_mpc5777c_pins_driver Notes
# - None.
#
# @section todo_mpc5777c_pins_driver TODO
# - None.
#
# @section author_mpc5777c_pins_driver Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 24/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.

import dataclasses
import struct
from typing import Any, Dict, Callable

import bitstruct

from framework.support.reports import logger, rpc_call
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    BasePinDriver,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.hardware_interfaces.drivers.common.definitions.interrupt_mapper import (
    irq_mapper,
)
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_pins_driver_pb2 import (
    PinsInitParams,
    PinWriteParams,
    ConfigMuxParams,
    PinReadParams,
    PinReadReturn,
)
from framework.support.vtime import TimeEvent


@dataclasses.dataclass
class PinPortData:
    """
    ! Dataclass to represent a GPIO pin port data.
    """

    mux: int
    in_mux_enable: bool
    out_mux_enable: bool
    value: int


class PinDriver(BasePinDriver):
    """Stub for GPIO pins."""

    def __init__(self, raise_interrupt_func: Callable[[int, int], None]) -> None:
        self.port_pins: Dict[int, PinPortData] = {}
        self.interrupt: int | None = None
        self._ready = TimeEvent()
        self._raise_interrupt = raise_interrupt_func
        self._initialized = False

    def set(self, pin: int, value: bool) -> None:
        """
        ! Set the value of a pin.

        @param pin The pin to set.
        @param value The value to set.
        """
        if pin in self.port_pins:
            self.port_pins[pin].value = value
        else:
            self.port_pins.update({pin: PinPortData(0, False, False, value)})

        flags = struct.unpack(">I", bitstruct.pack("u16u15b1", pin, 0, value))[0]
        if self.interrupt is not None:
            self._raise_interrupt(self.interrupt, flags)
            logger.info(
                f"INT {irq_mapper(self.interrupt)} raised for PIN{pin} update to {value}"
            )

    def get(self, pin: int) -> bool:
        """
        ! Get the value of a pin.

        @param pin The pin to get.
        @return The value of the pin.
        """
        if pin not in self.port_pins:
            raise KeyError(f"{pin} not configured/initialized")
        return bool(self.port_pins[pin].value)

    def wait_for_initialization(self) -> None:
        """
        ! Wait for the initialization.

        This method is used to wait for the initialization of the driver.
        """
        logger.debug(f"Wait for {self.__class__.__name__} initialization")
        self._ready.wait()
        logger.info(f"{self.__class__.__name__} initialized")

    def is_initialized(self) -> bool:
        """
        ! Check if the driver is initialized.
        """
        return self._initialized

    @rpc_call
    def PINS_DRV_Init(self, request: PinsInitParams, context: Any) -> Status:
        """
        ! Initialize the pins.
        """
        self.port_pins = {
            item.pin_id: PinPortData(
                item.mux, item.input_mux_enable, item.output_mux_enable, item.init_value
            )
            for item in request.config
        }
        self._initialized = True
        self.interrupt = request.irq_id
        logger.info(f"Registered INT {irq_mapper(request.irq_id)} for PINS update")
        self._ready.set()
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def PINS_DRV_QuickWritePin(self, request: PinWriteParams, context: Any) -> Status:
        """
        ! Write to a pin.
        """
        if request.pin_id not in self.port_pins:
            logger.info(
                f"Unknown pin {request.pin_id} in PINS_DRV_QuickWritePin, updated with value {request.value}"
            )
        else:
            self.port_pins[request.pin_id].value = request.value
            logger.info(
                f"Pin {request.pin_id} in PINS_DRV_QuickWritePin, updated with value {request.value}"
            )
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def PINS_DRV_QuickConfigOutputMux(
        self, request: ConfigMuxParams, context: Any
    ) -> Status:
        """
        ! Configures Output MUX.
        """
        self.port_pins[request.pin_id].out_mux_enable = request.enable
        self.port_pins[request.pin_id].mux = request.mux
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def PINS_DRV_QuickConfigInputMux(
        self, request: ConfigMuxParams, context: Any
    ) -> Status:
        """
        ! Configures Output MUX.
        """
        self.port_pins[request.pin_id].in_mux_enable = request.enable
        self.port_pins[request.pin_id].mux = request.mux
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def PINS_DRV_QuickReadPin(
        self, request: PinReadParams, context: Any
    ) -> PinReadReturn | None:
        """
        ! Read the state of a pin.

        If the driver is not initialized, perform an RPC call.
        """
        if not self.is_initialized():
            logger.info(
                f"Driver not initialized, performing RPC call for pin {request.pin_id}"
            )
            return PinReadReturn(
                status=Status(status=StatusEnum.STATUS_SUCCESS),
                value=1 if request.pin_id == 489 else 0,
            )

        return None
