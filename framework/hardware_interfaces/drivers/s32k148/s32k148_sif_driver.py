from typing import Any, Dict, Callable

from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    BaseSifDriver,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.support.reports import rpc_call, logger
from framework.hardware_interfaces.protoc.s32k148.s32k148_sif_driver_pb2_grpc import (
    SifDriverServicer,
)
from framework.hardware_interfaces.protoc.s32k148.s32k148_sif_driver_pb2 import (
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

    def read(self, size: int) -> bytes:
        """
        ! Read the data.
        """
        logger.debug(f"ADXL346 Read: {size} bytes")
        if self.instance_id == 0 and self.address == 1:
            if self._register == 0xBC:
                # logger.warning("returning orientation")
                return bytes([0x4E, 0])
            return bytes([0xE6, 0])  # Device ID for ADXL346
        if self.instance_id == 2 and self.address == 0:
            return bytes([0xFF] * size)
        raise NotImplementedError("read")

    def write(self, data: bytes) -> None:
        """
        ! Write the data.
        """
        logger.debug(f"instance id: {self.instance_id}, address: {self.address}")
        if self.instance_id == 0 and self.address == 1:
            logger.debug(f"ADXL346 Write: {data.hex()}")
            self._register = data[1]


class SifDriver(SifDriverServicer, BaseSifDriver):
    """
    ! SIF driver.
    """

    def __init__(self, raise_interrupt_func: Callable[[int, int], None]) -> None:
        self._sync_interfaces: Dict[int, Dict[int, SynchronousIfDevice]] = {}
        self._raise_interrupt = raise_interrupt_func

    def register_device(self, device: SynchronousIfDevice) -> None:
        """
        ! Register a device.
        """
        if device.instance_id not in self._sync_interfaces:
            self._sync_interfaces[device.instance_id] = {}

        self._sync_interfaces[device.instance_id][device.address] = device

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
