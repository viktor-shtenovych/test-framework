"""! @brief Interrupts declaration for accessing HW interrupts."""
##
# @file interrupts.py
#
# @brief Interrupts declaration for accessing HW interrupts.
#
# @section description_interrupts Description
# This module represents the IrqId and the Interrupts classes.
#
# @section libraries_interrupts Libraries/Modules
# - typing standard library (https://docs.python.org/3/library/typing.html)
# - queue standard library
# - enum standard library
# - dataclasses standard library
# - vtime module (local)
# - hardware_interfaces module (local)
#   - Access to InterruptContext class.
#   - Access to IdleContext class.
#   - Access to InterruptContextQueue class.
#   - Access to InterruptsServicer class.
#
# @section notes_interrupts Notes
# - None.
#
# @section todo_interrupts TODO
# - None.
#
# @section author_interrupts Author(s)
# - Created by:
#   - Lubos Kocvara <lubos.kocvara@globallogic.com> on 30/04/2024.
# - Modified by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 09/09/2024.
#   - Maksym Masalov maksym.masalov@globallogic.com on 12/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.

import dataclasses

from enum import IntEnum
from queue import Empty
from typing import Any

from framework.support.reports import logger, rpc_call
from framework.support.reports.log import measure_duration
from framework.support.vtime.queue import Queue
from framework.support.vtime import vtime_manager
from framework.support.vtime import get_worker_manager, VirtualTimeWorker
from framework.hardware_interfaces.drivers.common.definitions.interrupt_mapper import (
    irq_mapper,
)
from framework.hardware_interfaces.protoc.common.interrupts_pb2 import (
    InterruptContext,
    IdleContext,
    InterruptContextQueue,
)
from framework.hardware_interfaces.protoc.common.interrupts_pb2_grpc import (
    InterruptsServicer,
)


class IrqId(IntEnum):
    """! Interrupt type definition from `drivers/emu_s32k148/inc/S32K148.h`."""

    NotAvail_IRQn = -128
    NonMaskableInt_IRQn = -14
    HardFault_IRQn = -13
    MemoryManagement_IRQn = -12
    BusFault_IRQn = -11
    UsageFault_IRQn = -10
    SVCall_IRQn = -5
    DebugMonitor_IRQn = -4
    PendSV_IRQn = -2
    SysTick_IRQn = -1

    # Interrupt type definition from drivers/emu_mpc5777c/inc/mpc5777c.h
    PIT_RTI0_IRQn = 301


@dataclasses.dataclass
class Interrupt:
    """! Dataclass to represent an interrupt."""

    irq_id: IrqId | int
    flags: int = 0


class Interrupts(InterruptsServicer):
    """! A class to represent interrupts."""

    def __init__(self, use_worker_id: int = 0) -> None:
        self._interrupts: Queue[Interrupt] = Queue()
        self._worker_id = use_worker_id

    def start(self) -> None:
        """! Register worker in worker manager and go active."""
        get_worker_manager().register_worker(self._worker_id)
        get_worker_manager().go_active(self._worker_id)

    def stop(self) -> None:
        """! Unregister worker from worker manager."""
        get_worker_manager().unregister_worker(self._worker_id)

    def raise_interrupt(self, interrupt: IrqId | int, flags: int = 0) -> None:
        """! Schedule interrupt in queue.

        @param interrupt  The interrupt.
        @param flags  The flags. Defaults to 0.
        """
        logger.debug(
            f"Scheduling raising interrupt: {irq_mapper(interrupt)} (flags: {flags})"
        )
        self._interrupts.put(Interrupt(interrupt, flags))

    @VirtualTimeWorker.set_worker_id  # type: ignore
    @measure_duration
    def wait_for_interrupt(self) -> Interrupt:
        """! Waiting for an interrupt.

        In case no interrupt is scheduled then wait for defined 'virtual' vtime. In case of timeout (i.e. virtual vtime
        was increased) raise a SysTick interrupt with current virtual vtime.

        @return  Interrupt scheduled in queue (first in - first out).
        """
        try:
            logger.debug("Waiting for interrupt")
            start_time = vtime_manager.time_ms()
            irq = self._interrupts.get()
            if vtime_manager.time_ms() > (start_time + 1):
                logger.fatal(
                    f"Virtual vtime step more than 1 millisecond ({start_time} -> {vtime_manager.time_ms()}) (for unit tests this can be ok)"
                )
            logger.debug(f"Interrupt {irq_mapper(irq.irq_id)} raised")
            return irq
        except Empty:
            ## Exception is raised when timeout is reached. By that vtime virtual vtime manager shall execute
            ## `_clock_updated` method which add SysTick interrupt in queue
            return self._interrupts.get()

    @rpc_call
    def WaitForInterrupt(
        self, request: IdleContext, context: Any
    ) -> InterruptContextQueue:
        """! Wait for interrupt.

        @param request  The idle context.
        @param context  The context.

        @return  The interrupt context queue.
        """
        interrupt_context_queue = InterruptContextQueue()
        systick_irq_skip_count = request.idle_cycles
        non_systick_irq_happened = False

        while True:
            interrupt = self.wait_for_interrupt()
            interrupt_context = InterruptContext(
                irq_id=interrupt.irq_id,
                irq_flags=interrupt.flags,
                time=vtime_manager.time_us(),
            )
            interrupt_context_queue.queue.append(interrupt_context)
            if (
                interrupt.irq_id == IrqId.SysTick_IRQn
                or interrupt.irq_id == IrqId.PIT_RTI0_IRQn
            ):
                systick_irq_skip_count -= 1
            else:
                non_systick_irq_happened = True
            ##   Collecting interrupts until all SysTick interrupts that
            ## emulator can skip happened and interrupt queue is empty,
            ## or non systick interrupt happened and queue is empty.
            ##   Interrupt queue empty most likely because all interrupts
            ## with current time already happened.
            if self._is_interrupt_queue_empty() and (
                (systick_irq_skip_count <= 0) or non_systick_irq_happened
            ):
                break

        return interrupt_context_queue

    def _is_interrupt_queue_empty(self) -> bool:
        """! Check if interrupt queue is empty.

        @return True if interrupt queue is empty, False otherwise.
        """
        return self._interrupts.empty()

    def getsize(self) -> int:
        """! Get interrupts queue size.

        @return  Size of interrupt queue.
        """
        return self._interrupts.qsize()
