"""! @Brief: Synchronous interface device."""

##
# The SynchronousIfDevice class is a class that represents a synchronous interface device.
# @file mpc5777c_sif_driver.py
#
# @section description_mpc5777c_sif_driver Description
# This module represents the SynchronousIfDevice class.
#
# @section libraries_mpc5777c_sif_driver Libraries/Modules
# - grpc standard library (https://grpc.io/docs/languages/python/)
# - SynchronousIfDevice module (local)
#   - Access to SynchronousIfDevice class.
#
# @section notes_mpc5777c_sif_driver Notes
# - None.
#
# @section todo_mpc5777c_sif_driver TODO
# - None.
#
# @section author_mpc5777c_sif_driver Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 24/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.
from typing import Any, Dict, Callable

from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    BaseSifDriver,
)
from framework.support.vtime import TimeEvent
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.support.reports import rpc_call, logger
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_sif_driver_pb2_grpc import (
    SifDriverServicer,
)
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_sif_driver_pb2 import (
    SifInitParams,
    SifReadParams,
    SifWriteParams,
    SifReadReturns,
)


class SynchronousIfDevice:
    """
    ! A synchronous interface device.
    """

    def __init__(self, instance_id: int, address: int) -> None:
        self.instance_id = instance_id
        self.address = address

        self.irq_id: int | None = None
        self.eoq_irq_id: int | None = None
        self.fault_irq_id: int | None = None

        self._register = 0x00

        self._data = {
            0x00: [0xE6, 0x00],
            0x2E: [0x00, 0x00],
            0x2D: [0xFF, 0x00],
            0x3C: [0x4B, 0x00],
        }

    def set_irq(self, irq_id: int) -> None:
        """
        ! Set the IRQ.
        """
        self.irq_id = irq_id

    def set_eoq_irq(self, irq_id: int) -> None:
        """
        ! Set the EOQ IRQ.
        """
        self.eoq_irq_id = irq_id

    def set_fault_irq(self, irq_id: int) -> None:
        """
        ! Set the fault IRQ.
        """
        self.fault_irq_id = irq_id

    def read(self, size: int) -> bytes:
        """
        ! Read the data.
        """
        raise NotImplementedError("Read not implemented")

    def write(self, data: bytes) -> None:
        """
        ! Write the data.
        """
        logger.debug(f"instance id: {self.instance_id}, address: {self.address}")
        if self.instance_id == 0 and self.address == 1:
            self._register = data[1]


class SifDriver(SifDriverServicer, BaseSifDriver):
    """
    ! SIF driver.
    """

    def __init__(self, raise_interrupt_func: Callable[[int, int], None]) -> None:
        self._sync_interfaces: Dict[int, Dict[int, SynchronousIfDevice]] = {}
        self._ready = TimeEvent()
        self._raise_interrupt = raise_interrupt_func

    def register_device(self, device: SynchronousIfDevice) -> None:
        """
        ! Register a device.
        """
        if device.instance_id not in self._sync_interfaces:
            self._sync_interfaces[device.instance_id] = {}

        self._sync_interfaces[device.instance_id][device.address] = device

    def wait_for_initialization(self) -> None:
        """! Wait for initialization."""
        logger.debug(f"Waiting for {self.__class__.__name__} initialization.")
        self._ready.wait(0.01)
        logger.info(f"{self.__class__.__name__} initialized.")

    @rpc_call
    def SIF_DRV_Init(self, request: SifInitParams, context: Any) -> Status:
        """
        ! Initialize the driver.
        """
        for device in self._sync_interfaces[request.instance].values():
            logger.debug(
                f"Setting IRQ for {device.instance_id}/{device.address} to {request.irq_id}"
            )
            device.set_irq(irq_id=request.irq_id)
        logger.debug(f"SIF_DRV_Init: {request.instance}")
        self._ready.set()
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def SIF_DRV_Write(self, request: SifWriteParams, context: Any) -> Status:
        """
        ! Write to the device.
        """
        logger.debug(
            f"SIF_DRV_Write if:{request.instance} / {request.periph_id} : {request.message.hex()}"
        )
        if request.periph_id not in self._sync_interfaces[request.instance]:
            logger.error(
                f"Peripheral {request.periph_id} for {request.instance} not configured"
            )
            return Status(status=StatusEnum.STATUS_SUCCESS)
        device = self._sync_interfaces[request.instance][request.periph_id]

        try:
            device.write(request.message)

            if request.irq_required and device.irq_id is not None:
                self._raise_interrupt(device.irq_id, 0)

            return Status(status=StatusEnum.STATUS_SUCCESS)
        except TimeoutError:
            return Status(status=StatusEnum.STATUS_TIMEOUT)

    @rpc_call
    def SIF_DRV_Read(self, request: SifReadParams, context: Any) -> SifReadReturns:
        """
        ! Read from the device.
        """
        logger.debug(
            f"SIF_DRV_Read{request.instance} / {request.periph_id} (size: {request.size})"
        )
        if request.periph_id not in self._sync_interfaces[request.instance]:
            logger.error(f"peripheral {request.periph_id} not configured")
            response = SifReadReturns(
                status=Status(status=StatusEnum.STATUS_SUCCESS),
                message=bytes([0xFF] * request.size),
            )
            return response

        device = self._sync_interfaces[request.instance][request.periph_id]

        try:
            data = device.read(request.size)

            response = SifReadReturns(
                status=Status(status=StatusEnum.STATUS_SUCCESS), message=data
            )
            return response
        except TimeoutError:
            return SifReadReturns(
                status=Status(status=StatusEnum.STATUS_TIMEOUT), message=None
            )
