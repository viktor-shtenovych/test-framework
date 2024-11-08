"""! @Brief FlexCAN driver implementation for the CAN driver."""

#
# @file flexcan_driver.py
#
# @brief FlexCAN driver implementation for the CAN driver.
#
# @section description_flexcan_driver Description
# This module represents the FlexCanDriver class.
#
# @section libraries_flexcan_driver Libraries/Modules
# - typing standard library (https://docs.python.org/3/library/typing.html)
# - queue standard library
# - enum standard library
# - dataclasses standard library
# - vtime module (local)
# - hardware_interfaces module (local)
#   - Access to CanBus class.
#   - Access to CanMessage class.
#   - Access to CanBuffer class.
#   - Access to FlexCanDriverServicer class.
#   - Access to Status class.
#   - Access to StatusEnum class.
#   - Access to FCSendParams class.
#   - Access to FCFreezeModeParams class.
#   - Access to FCInitParams class.
#   - Access to FCMsgIdType class.
#   - Access to FCReceiveReqParams class.
#   - Access to FCConfigRxMbParams class.
#   - Access to FCSetRxIndMaskParams class.
#   - Access to FCGetReceivedDataParams class.
#   - Access to FCGetReceivedDataReturn class.
#   - Access to FCIrqFlags class.
#
# @section notes_flexcan_driver Notes
# - None.
#
# @section todo_flexcan_driver TODO
# - None.
#
# @section author_flexcan_driver Author(s)
#   - Lubos Kocvara <lubos.kocvara@globallogic.com> on 30/04/2024.
# - Modified by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 02/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.
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
from framework.hardware_interfaces.protoc.common.flexcan_driver_pb2_grpc import (
    FlexCanDriverServicer,
)
from framework.hardware_interfaces.protoc.common.flexcan_driver_pb2 import (
    FCSendParams,
    FCFreezeModeParams,
    FCInitParams,
    FCMsgIdType,
    FCReceiveReqParams,
    FCConfigRxMbParams,
    FCSetRxIndMaskParams,
    FCGetReceivedDataParams,
    FCGetReceivedDataReturn,
    FCIrqFlags,
)
from framework.support.vtime import TimeEvent


class FlexCanDriver(CanBus, FlexCanDriverServicer):
    """! Support for CAN bus access + stub for FootSwitch CAN driver."""

    def __init__(self, raise_interrupt_func: Callable[[int, int], None]) -> None:
        self.raise_interrupt = raise_interrupt_func
        self.instances: Dict[int, CANInstance] = {}
        self._ready = TimeEvent()

    def _initialize_instance(self, instance_id: int, irq_id: int) -> None:
        """! Helper function to initialize a new instance."""
        if instance_id not in self.instances:
            self.instances[instance_id] = CANInstance(
                in_msgs=Queue(),
                out_buffers={},
                freeze_mode=False,
                irq_id=irq_id,
                read_request_pending={},
            )
            logger.info(
                f"New FlexCAN instance {instance_id} created with IRQ {irq_mapper(irq_id)}"
            )

    def get_instance(self, instance_id: int) -> CANInstance:
        """! Helper function to retrieve an instance."""
        if instance_id not in self.instances:
            raise ValueError(f"FlexCAN instance {instance_id} not initialized")
        return self.instances[instance_id]

    def send(
        self, msg: CanMessage, timeout: float | None = None, instance_id: int = 0
    ) -> None:
        """
        Send a message on the bus.
        """
        instance = self.get_instance(instance_id)
        for mb_idx, buffer in instance.out_buffers.items():
            if buffer.put_can_msg(msg, timeout=timeout):
                buffer.read_request.wait(timeout)
                self.raise_interrupt(
                    instance.irq_id,
                    (mb_idx << 16) | FCIrqFlags.FCIrqFlags_RX_COMPLETE,
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

    # FlexCanDrv methods

    @rpc_call
    def FLEXCAN_DRV_Init(self, request: FCInitParams, context: Any) -> Status:
        """
        ! Initialize the driver.
        """
        self._initialize_instance(request.instance_id, request.irq_id)
        logger.info(
            f"FlexCAN driver initialized with IRQ {irq_mapper(request.irq_id)}, instance {request.instance_id}"
        )
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def FLEXCAN_DRV_EnterFreezeMode(
        self, request: FCFreezeModeParams, context: Any
    ) -> Status:
        """
        ! Enter freeze mode.
        """
        instance = self.get_instance(request.instance_id)
        instance.freeze_mode = True
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def FLEXCAN_DRV_ExitFreezeMode(
        self, request: FCFreezeModeParams, context: Any
    ) -> Status:
        """
        ! Exit freeze mode.
        """
        instance = self.get_instance(request.instance_id)
        instance.freeze_mode = False
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def FLEXCAN_DRV_Send(self, request: FCSendParams, context: Any) -> Status:
        """
        ! Send a message.
        """
        msg = CanMessage(
            arbitration_id=request.msg_id,
            data=request.mb_data,
            is_extended_id=request.msg_id_type == FCMsgIdType.FCMsgIdType_EXT,
        )

        instance = self.get_instance(request.instance_id)
        instance.in_msgs.put(msg)
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def FLEXCAN_DRV_SetRxIndividualMask(
        self, request: FCSetRxIndMaskParams, context: Any
    ) -> Status:
        """
        ! Set the mask for a receive buffer.
        """
        instance = self.get_instance(request.instance_id)
        if request.mb_idx not in instance.out_buffers:
            instance.out_buffers[request.mb_idx] = CanBuffer(request.mb_idx)

        instance.out_buffers[request.mb_idx].set_mask(request.mask)
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def FLEXCAN_DRV_ConfigRxMb(
        self, request: FCConfigRxMbParams, context: Any
    ) -> Status:
        """
        ! Configure a receive buffer.
        """
        instance = self.get_instance(request.instance_id)
        instance.out_buffers[request.mb_idx].set_filter(request.msg_id)
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def FLEXCAN_DRV_ReceiveReq(
        self, request: FCReceiveReqParams, context: Any
    ) -> Status:
        """
        ! Request a receive.
        """
        instance = self.get_instance(request.instance_id)
        instance.out_buffers[request.mb_idx].read_request.set()
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def FLEXCAN_DRV_GetReceivedData(
        self, request: FCGetReceivedDataParams, context: Any
    ) -> FCGetReceivedDataReturn:
        """
        ! Get the received data.
        """
        instance = self.get_instance(request.instance_id)
        msg: CanMessage = instance.out_buffers[request.mb_idx].get_nowait()

        return FCGetReceivedDataReturn(
            status=Status(status=StatusEnum.STATUS_SUCCESS),
            instance_id=request.instance_id,
            msg_id=msg.arbitration_id,
            mb_data=bytes(msg.data),
        )
