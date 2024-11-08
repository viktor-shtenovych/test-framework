"""! @Brief MCAN driver for MPC5777C."""
#
# @file mpc5777c_mcan_driver.py
#
# @brief MCAN driver for MPC5777C.
#
# @section description_mpc5777c_mcan_driver Description
# This module represents the MCANDriver class.
#
# @section libraries_mpc5777c_mcan_driver Libraries/Modules
# - dataclasses standard library
# - queue standard library
# - typing standard library
# - Empty class from queue module
# - Any class from typing module
# - Callable class from typing module
# - Dict class from typing module
# - CanBuffer class from framework/hardware_interfaces/drivers/common/definitions/can_buffer module
# - irq_mapper function from framework/hardware_interfaces/drivers/common/definitions/interrupt_mapper module
# - rpc_call function from framework/support/reports module
# - logger function from framework/support/reports module
# - CanBus class from framework/hardware_interfaces/drivers/common/definitions/interfaces module
# - CanMessage class from framework/hardware_interfaces/drivers/common/definitions/interfaces module
# - TimeEvent class from framework/support/vtime module
# - MCANInstance class from framework/hardware_interfaces/drivers/mpc5777c/mpc5777c_mcan_driver module
# - MCInitParams class from framework/hardware_interfaces/protoc/mpc5777c/mpc5777c_mcan_driver_pb2 module
# - MCSetRxFifoFiletrMaskParams class from framework/hardware_interfaces/protoc/mpc5777c/mpc5777c_mcan_driver_pb2 module
# - MCReceiveReqParams class from framework/hardware_interfaces/protoc/mpc5777c/mpc5777c_mcan_driver_pb2 module
# - MCGetReceivedDataParams class from framework/hardware_interfaces/protoc/mpc5777c/mpc5777c_mcan_driver_pb2 module
# - MCGetReceivedDataReturn class from framework/hardware_interfaces/protoc/mpc5777c/mpc5777c_mcan_driver_pb2 module
# - MCIrqFlags class from framework/hardware_interfaces/protoc/mpc5777c/mpc5777c_mcan_driver_pb2 module
# - MCMsgIdType class from framework/hardware_interfaces/protoc/mpc5777c/mpc5777c_mcan_driver_pb2 module
# - MCMode class from framework/hardware_interfaces/protoc/mpc5777c/mpc5777c_mcan_driver_pb2 module
# - MCANInstance class from framework/hardware_interfaces/drivers/mpc5777c/mpc5777c_mcan_driver module
#
# @section notes_mpc5777c_mcan_driver Notes
# - None.
#
# @section todo_mpc5777c_mcan_driver TODO
# - None.
#
# @section author_mpc5777c_mcan_driver Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 29/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved

from queue import Empty
from typing import Any, Callable, Dict

from framework.hardware_interfaces.drivers.common.definitions.can_buffer import (
    CanBuffer,
)
from framework.hardware_interfaces.drivers.common.definitions.can_instance import (
    CANInstance,
)
from framework.hardware_interfaces.drivers.common.definitions.interrupt_mapper import (
    irq_mapper,
)
from framework.support.reports import rpc_call, logger
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    CanBus,
    CanMessage,
)
from framework.support.vtime.queue import Queue
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum

from framework.support.vtime import TimeEvent
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_mcan_driver_pb2_grpc import (
    MCanDriverServicer,
)
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_mcan_driver_pb2 import (
    MCSendParams,
    MCInitParams,
    MCSetRxFifoFiletrMaskParams,
    MCReceiveReqParams,
    MCGetReceivedDataParams,
    MCGetReceivedDataReturn,
    MCIrqFlags,
    MCMsgIdType,
    MCMode,
)


class MCANDriver(CanBus, MCanDriverServicer):
    """! Support for CAN bus access + stub for MCAN driver."""

    def __init__(self, raise_interrupt_func: Callable[[int, int], None]) -> None:
        self.raise_interrupt = raise_interrupt_func
        self.instances: Dict[int, CANInstance] = {}
        self._ready = TimeEvent()

    def _initialize_instance(self, instance_id: int, irq_id: int) -> None:
        """
        ! Initialize MCAN instance.
        """
        if instance_id not in self.instances:
            self.instances[instance_id] = CANInstance(
                in_msgs=Queue(),
                out_buffers={},
                freeze_mode=MCMode.MC_NORMAL_MODE,
                irq_id=irq_id,
                read_request_pending={},
            )
            logger.info(
                f"New MCAN instance {instance_id} created with IRQ {irq_mapper(irq_id)}"
            )

    def get_instance(self, instance_id: int) -> CANInstance:
        """
        ! Get MCAN instance.
        """
        if instance_id not in self.instances:
            raise ValueError(f"MCAN instance {instance_id} not initialized")
        return self.instances[instance_id]

    def send(
        self, msg: CanMessage, timeout: float | None = None, instance_id: int = 0
    ) -> None:
        """
        ! Send a message on the bus.
        """
        instance = self.get_instance(instance_id)
        for mb_idx, buffer in instance.out_buffers.items():
            if buffer.put_can_msg(msg, timeout=timeout):
                buffer.read_request.wait(timeout)
                self.raise_interrupt(
                    instance.irq_id, MCIrqFlags.MCIrqFlags_RX0FIFO_COMPLETE << 8
                )
                buffer.read_request.clear()

    def recv(
        self, timeout: float | None = None, instance_id: int = 0
    ) -> CanMessage | None:
        """
        ! Receive a message from the bus.
        """
        instance = self.get_instance(instance_id)
        try:
            msg: CanMessage | Any = instance.in_msgs.get(timeout=timeout)
            self.raise_interrupt(MCIrqFlags.MCIrqFlags_RX0FIFO_COMPLETE, 0)
            return msg
        except Empty:
            raise TimeoutError(f"No data received within {timeout}")

    def wait_for_initialization(self) -> None:
        """
        ! Wait for initialization.
        """
        logger.debug(f"Wait for {self.__class__.__name__} initialization")
        self._ready.wait(0.01)
        logger.info(f"{self.__class__.__name__} initialized")

    @rpc_call
    def MCAN_DRV_Init(self, request: MCInitParams, context: Any) -> Status:
        """
        ! Initialize the MCAN driver.
        """
        self._initialize_instance(request.instance_id, request.irq_id)
        logger.info(
            f"MCan driver initialized with IRQ {irq_mapper(request.irq_id)}, instance {request.instance_id}"
        )
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def MCAN_DRV_Send(self, request: MCSendParams, context: Any) -> Status:
        """
        ! Send a message on the bus.
        """
        msg = CanMessage(
            arbitration_id=request.msg_id,
            data=request.mb_data,
            is_extended_id=request.msg_id_type == MCMsgIdType.MCMsgIdType_EXT,
        )

        instance = self.get_instance(request.instance_id)
        instance.in_msgs.put(msg)
        logger.info(
            f"Message sent on instance {request.instance_id}: ID={request.msg_id}"
        )
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def MCAN_DRV_SetRxFifoFilterMask(
        self, request: MCSetRxFifoFiletrMaskParams, context: Any
    ) -> Status:
        """
        ! Set RX FIFO filter mask.
        """
        instance = self.get_instance(request.instance_id)
        if request.fl_idx not in instance.out_buffers:
            instance.out_buffers[request.fl_idx] = CanBuffer(request.fl_idx)

        instance.out_buffers[request.fl_idx].set_mask(request.mask)
        logger.info(
            f"Set RX FIFO filter mask for instance {request.instance_id}, filter={request.fl_idx}"
        )
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def MCAN_DRV_ReceiveReq(self, request: MCReceiveReqParams, context: Any) -> Status:
        """
        ! Receive request.
        """
        instance = self.get_instance(request.instance_id)
        instance.out_buffers[request.vmb_idx] = CanBuffer(request.vmb_idx)
        instance.out_buffers[request.vmb_idx].read_request.set()
        logger.info(
            f"Receive request set for instance {request.instance_id}, buffer={request.vmb_idx}"
        )
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def MCAN_DRV_GetReceivedData(
        self, request: MCGetReceivedDataParams, context: Any
    ) -> MCGetReceivedDataReturn:
        """
        ! Get received data.
        """
        try:
            instance = self.get_instance(request.instance_id)
            msg: CanMessage = instance.out_buffers[request.vmb_idx].get_nowait()

            return MCGetReceivedDataReturn(
                status=Status(status=StatusEnum.STATUS_SUCCESS),
                instance_id=request.instance_id,
                msg_id=msg.arbitration_id,
                mb_data=bytes(msg.data),
            )
        except Empty:
            return MCGetReceivedDataReturn(
                status=Status(status=StatusEnum.STATUS_ERROR),
                instance_id=request.instance_id,
            )
