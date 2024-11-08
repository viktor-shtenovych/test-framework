from concurrent.futures import ThreadPoolExecutor
from typing import Iterator, List

import pytest
from pytest_check import check

from framework.hardware_interfaces.drivers.common.interrupts import Interrupts, IrqId
from framework.support.reports import logger
from framework.support.vtime import (
    VirtualTimeThreadPoolExecutor,
)


@pytest.fixture(scope="module")
def irq_mgr() -> Iterator[Interrupts]:
    """! Initialize and start the Interrupts manager.

    @return Interrupts  An instance of the Interrupts class.
    """
    _irq_mgr = Interrupts()

    _irq_mgr.start()
    yield _irq_mgr
    _irq_mgr.stop()


@pytest.mark.parametrize(
    "interrupts",
    [
        [
            IrqId.NotAvail_IRQn,
            IrqId.NonMaskableInt_IRQn,
            IrqId.HardFault_IRQn,
            IrqId.MemoryManagement_IRQn,
            IrqId.BusFault_IRQn,
            IrqId.UsageFault_IRQn,
            IrqId.SVCall_IRQn,
            IrqId.DebugMonitor_IRQn,
            IrqId.PendSV_IRQn,
            IrqId.SysTick_IRQn,
        ]
    ],
)
def test_raising_interrupts(interrupts: List[int], irq_mgr: Interrupts) -> None:
    """! Verify raising interrupts when using ThreadPoolExecutor/VirtualTimeThreadPoolExecutor.

    Check that raised interrupts are returned when `wait_for_interrupt` is executed.
    """
    for interrupt in interrupts:
        with (
            ThreadPoolExecutor(max_workers=10) as emulator_executor,
            VirtualTimeThreadPoolExecutor(max_workers=10) as tb_executor,
        ):
            tb_executor.submit(lambda: irq_mgr.raise_interrupt(interrupt)).result()
            with check:
                assert (
                    emulator_executor.submit(irq_mgr.wait_for_interrupt).result().irq_id
                    == interrupt
                ), (
                    f"Interrupt not raised: {interrupt}; Actual: "
                    f"{emulator_executor.submit(irq_mgr.wait_for_interrupt).result().irq_id}"
                )


@pytest.mark.parametrize(
    "interrupts",
    [
        [
            IrqId.NotAvail_IRQn,
            IrqId.NonMaskableInt_IRQn,
            IrqId.HardFault_IRQn,
            IrqId.MemoryManagement_IRQn,
            IrqId.BusFault_IRQn,
            IrqId.UsageFault_IRQn,
            IrqId.SVCall_IRQn,
            IrqId.DebugMonitor_IRQn,
            IrqId.PendSV_IRQn,
            IrqId.SysTick_IRQn,
        ]
    ],
)
def test_raising_interrupts_in_main_thread(
    interrupts: List[int], irq_mgr: Interrupts
) -> None:
    """! Verify raising interrupts when interrupts are generated in main thread.

    Check that raised interrupts are returned when `wait_for_interrupt` is executed.
    """
    for interrupt in interrupts:
        with ThreadPoolExecutor(max_workers=10) as emulator_executor:
            irq_mgr.raise_interrupt(interrupt)
            with check:
                assert (
                    emulator_executor.submit(irq_mgr.wait_for_interrupt).result().irq_id
                    == interrupt
                ), (
                    f"Interrupt not raised: {interrupt}; Actual: "
                    f"{emulator_executor.submit(irq_mgr.wait_for_interrupt).result().irq_id}"
                )


@pytest.mark.parametrize(
    "interrupts",
    [
        [
            IrqId.NotAvail_IRQn,
            IrqId.NonMaskableInt_IRQn,
            IrqId.HardFault_IRQn,
            IrqId.MemoryManagement_IRQn,
            IrqId.BusFault_IRQn,
            IrqId.UsageFault_IRQn,
            IrqId.SVCall_IRQn,
            IrqId.DebugMonitor_IRQn,
            IrqId.PendSV_IRQn,
            IrqId.SysTick_IRQn,
        ]
    ],
)
def test_check_interrupts_queue_size(
    interrupts: List[int], irq_mgr: Interrupts
) -> None:
    """! Test verify if interrupts queue size is in correct sequence.

    Check  that raised interrupts are returned interrupts and size of interrupts in queue.

    @param interrupts  A list of input interrupts
    @param irq_mgr  The Interrupts class object
    """
    with ThreadPoolExecutor(max_workers=10) as emulator_executor:
        logger.info("Raise all interrupts")
        for interrupt in interrupts:
            irq_mgr.raise_interrupt(interrupt)

        interrupt_queue_size = irq_mgr.getsize()
        assert interrupt_queue_size == len(
            interrupts
        ), "Size of interrupts is not equal to size of queue!"

        logger.info(f"Waiting all {interrupt} in queue")
        for interrupt in interrupts:
            assert (
                emulator_executor.submit(irq_mgr.wait_for_interrupt).result().irq_id
                == interrupt
            ), f"Interrupt  {interrupt} not raised!"

        is_interrupt_queue_empty = irq_mgr.getsize()
        assert is_interrupt_queue_empty == 0, "Interrupt queue is not empty!"
