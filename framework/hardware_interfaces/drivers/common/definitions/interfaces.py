"""! @brief Interfaces declaration for accessing HW interfaces."""
##
# @file interfaces.py
#
# @brief Interfaces declaration for accessing HW interfaces.
#
# @section description_interfaces Description
# These interfaces shall be used by apps of HW peripherals e.g. battery, treadle, etc.
# Implementation of these interfaces is done in HW driver's stubs or HW specific libraries (like can python module)
#
# @section libraries_interfaces Libraries/Modules
# - typing standard library (https://docs.python.org/3/library/typing.html)
# - abc standard library
# - enum standard library
# - can standard library
# - dataclasses standard library
# - interrupts module (local)
#   - Access to IrqId class.
#
# @section notes_interfaces Notes
# - None.
#
# @section todo_interfaces TODO
# - None.
#
# @section author_interfaces Author(s)
# - Created by:
#   - Lubos Kocvara <lubos.kocvara@globallogic.com> on 03/04/2024.
# - Modified by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 02/07/2024.
#   - Maksym Masalov maksym.masalov@globallogic.com on 12/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.

from abc import ABC, abstractmethod
from typing import TypeAlias, Protocol, Any
from enum import IntEnum
from framework.support.reports import logger
from framework.support.vtime import TimeEvent

import can
import dataclasses

from framework.hardware_interfaces.drivers.common.interrupts import IrqId

CanBus: TypeAlias = can.BusABC
CanMessage: TypeAlias = can.Message


class TInterruptCallback(Protocol):
    """! Type alias for interrupt callback.

    The callback is called when an interrupt is triggered.
    """

    def __call__(self, irq_id: int | IrqId, flags: int = 0, /) -> None:
        """! Call the callback.

        @param irq_id  The IRQ ID.
        @param flags  The flags. Defaults to 0.
        """
        pass


class Pins(ABC):
    """! Interface for accessing GPIO pins."""

    @abstractmethod
    def set(self, *args: Any) -> None:
        """! Set the value of a pin.

        @param args with the port, pin and value
        """
        pass

    @abstractmethod
    def get(self, *args: Any) -> bool:
        """! Get the value of a pin.

        @param args with the port and pin

        @return The value of the pin.
        """
        pass


class FtmChannelABC(ABC):
    """! Interface for accessing FlexTimer channels.

    The FlexTimer channels are used to generate PWM signals.
    """

    instance: int
    channel: int
    irq_id: int

    @abstractmethod
    def start(self) -> None:
        """! Start the FlexTimer channel."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """! Stop the FlexTimer channel."""
        pass


class DataStream(ABC):
    """! Interface to by implemented by simulator of async and sync interface chip."""

    @abstractmethod
    def read(self) -> bytes:
        """! Read data from the stream.

        @return The data read from the stream.
        """
        pass

    @abstractmethod
    def write(self, data: bytes) -> None:
        """! Write data to the stream.

        @param data  The data to write to the stream.
        """
        pass


@dataclasses.dataclass
class AsyncInterfaceData:
    """! Data class for async interface.

    @param data_stream  The data stream.
    @param enabled  A flag to indicate whether the interface is enabled.
    @param irq_id  The IRQ ID.
    @param is_read_req  A flag to indicate whether the request is for reading.
    """

    data_stream: DataStream
    enabled: bool
    irq_id: int | None
    is_read_req: bool


class TimerManagerABC(ABC):
    """! Manages multiple independent timers."""

    @abstractmethod
    def create_timer(
        self, timer_id: int, irq_id: int, callback: TInterruptCallback
    ) -> None:
        """! Create a timer with a given ID and IRQ ID."""

    @abstractmethod
    def start_timer(self, timer_id: int) -> None:
        """! Start a timer by its ID."""

    @abstractmethod
    def stop_timer(self, timer_id: int) -> None:
        """! Stop a timer by its ID."""

    @abstractmethod
    def set_timer_period(self, timer_id: int, period_us: int) -> None:
        """! Set the period of a timer."""

    @abstractmethod
    def stop_all_timers(self) -> None:
        """! Stop all running timers."""


@dataclasses.dataclass
class PwmChannelABC(ABC):
    """! Abstract class for PWM channel."""

    instance: int
    channel: int
    polarity: int = 1
    period: int = 0
    duty_cycle: int = 0


class Access(IntEnum):
    """! Enumeration for access type."""

    R = 0
    RW = 1


class BaseSifDriver(ABC):
    """! Interface for accessing SifDriver."""


class BasePinDriver(Pins):
    """! Interface for accessing PinDriver."""

    def __init__(self) -> None:
        self._ready = TimeEvent()

    def wait_for_initialization(self) -> None:
        """! Waits for the initialization of the LPIT driver.

        This method logs the start of the wait, waits for the readiness signal,
        and then logs the completion of the initialization.
        """
        logger.debug(f"Wait for {self.__class__.__name__} initialization")
        self._ready.wait()
        logger.info(f"{self.__class__.__name__} initialized")

    def set(self, *args: Any) -> None:
        """! Set the value of a pin."""
        pass

    def get(self, *args: Any) -> bool:
        """! Get the value of a pin."""
        return False


class PITChannelManagerABC(ABC):
    """! Manages multiple independent timers."""

    @abstractmethod
    def create_channel(self, channel_id: int) -> None:
        """! Create a timer with a given ID and IRQ ID."""

    @abstractmethod
    def start_channel(self, channel_id: int) -> None:
        """! Start a timer by its ID."""

    @abstractmethod
    def stop_channel(self, channel_id: int) -> None:
        """! Stop a timer by its ID."""

    @abstractmethod
    def set_period_us(self, channel_id: int, period_us: int) -> None:
        """! Set the period of a timer (in microseconds)."""

    @abstractmethod
    def enable_interrupt(
        self, channel_id: int, irq_id: int, callback: TInterruptCallback
    ) -> None:
        """! Enable timer's interrupt."""

    @abstractmethod
    def disable_interrupt(self, channel_id: int) -> None:
        """! Disable timer's interrupt."""

    @abstractmethod
    def stop_all(self) -> None:
        """! Stop all running timers."""
