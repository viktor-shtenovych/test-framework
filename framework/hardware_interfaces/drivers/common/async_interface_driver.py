"""! @brief Defines the eSCI driver."""

##
# @file async_interface_driver.py
#
# @brief Defines the eSCI driver.
#
# @section description_async_interface_driver Description
# This module represents the AsyncInterfaceDriver class.
#
# @section libraries_pit_driver Libraries/Modules
# - grpc standard library (https://grpc.io/docs/languages/python/)
# - eSCI module (local)
#   - Access to AsyncInterfaceDriver class.
#
# @section async_interface_driver Notes
# - None.
#
# @section todo_async_interface_driver TODO
# - None.
#
# @section author_async_interface_driver Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 24/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.
from typing import Any, Dict, Callable

from framework.support.reports import rpc_call, logger
from framework.hardware_interfaces.protoc.common.async_interface_pb2 import (
    AIInitParams,
    AIInterfaceId,
    AIWriteReqParams,
    AIReadReqParams,
    AIGetReadDataReturn,
    AIIrqFlags,
)
from framework.hardware_interfaces.protoc.common.async_interface_pb2_grpc import (
    AsyncInterfaceServicer,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.support.vtime import TimeEvent
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    DataStream,
    AsyncInterfaceData,
)


class AsyncInterfaceDriver(AsyncInterfaceServicer):
    """
    Async interface driver.
    """

    def __init__(self, raise_interrupt_func: Callable[[int, int], None]) -> None:
        self.async_interfaces: Dict[int, AsyncInterfaceData] = {}
        self._ready = TimeEvent()
        self._raise_interrupt = raise_interrupt_func
        self.write_flag = False

    def register_stream(self, interface_id: int, data_stream: DataStream) -> None:
        """
        Register data stream for the given interface ID.

        Args:
            interface_id: Interface ID.
            data_stream: Data stream.
        """
        self.async_interfaces[interface_id] = AsyncInterfaceData(
            data_stream=data_stream, enabled=False, irq_id=None, is_read_req=False
        )

    def wait_for_initialization(self) -> None:
        """
        Wait for initialization.
        """
        logger.debug(f"Wait for {self.__class__.__name__} initialization")
        self._ready.wait(0.01)
        logger.info(f"{self.__class__.__name__} initialized")

    @rpc_call
    def AsyncInterface_Init(self, request: AIInitParams, context: Any) -> Status:
        """
        Initialize the async interface.

        Args:
            request: Initialization parameters.
            context: RPC context.
        """
        if request.interface_id in self.async_interfaces:
            self.async_interfaces[request.interface_id].irq_id = request.irq_id
            self.async_interfaces[request.interface_id].enabled = False
        else:
            raise AttributeError(
                f"Data stream not registered for {request.interface_id}"
            )

        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def AsyncInterface_Enable(self, request: AIInterfaceId, context: Any) -> Status:
        """
        Enable the async interface.

        Args:
            request: Interface ID.
            context: RPC context.
        """
        self.async_interfaces[request.interface_id].enabled = True
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def AsyncInterface_Disable(self, request: AIInterfaceId, context: Any) -> Status:
        """
        Disable the async interface.

        Args:
            request: Interface ID.
            context: RPC context.
        """
        self.async_interfaces[request.interface_id].enabled = False
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def AsyncInterface_ReadReq(self, request: AIReadReqParams, context: Any) -> Status:
        """
        Read request.

        Args:
            request: Read request parameters.
            context: RPC context.
        """
        self._ready.set()
        self.async_interfaces[request.interface_id].is_read_req = request.data_size > 0
        # interface = self.async_interfaces[request.interface_id]
        # data = interface.data_stream.read()
        #
        # if len(data) < request.data_size:
        #     assert interface.irq_id is not None
        #     self._raise_interrupt(interface.irq_id, AIIrqFlags.AIIrqFlags_RX_IDLE_LINE)
        # else:
        #     raise NotImplementedError(
        #         "Sending more data than requested is not supported yet."
        #     )
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def AsyncInterface_GetReadData(
        self, request: AIInterfaceId, context: Any
    ) -> AIGetReadDataReturn:
        """
        Get read data.

        Args:
            request: Interface ID.
            context: RPC context.
        """
        interface = self.async_interfaces[request.interface_id]
        data = interface.data_stream.read()
        self._is_read_req = False
        return AIGetReadDataReturn(
            status=Status(status=StatusEnum.STATUS_SUCCESS),
            data_bytes=data,
        )

    @rpc_call
    def AsyncInterface_WriteReq(
        self, request: AIWriteReqParams, context: Any
    ) -> Status:
        """
        Write request.

        Args:
            request: Write request parameters.
            context: RPC context.
        """
        if request.interface_id in self.async_interfaces:
            interface = self.async_interfaces[request.interface_id]
            if interface.enabled:
                assert interface.irq_id is not None
                interface.data_stream.write(request.data_bytes)
                self._raise_interrupt(interface.irq_id, AIIrqFlags.AIIrqFlags_TX_EMPTY)
                self.write_flag = True
                # TODO: fix this, should be only if there is a data in stream
                if self.async_interfaces[request.interface_id].is_read_req:
                    self._raise_interrupt(
                        interface.irq_id, AIIrqFlags.AIIrqFlags_RX_IDLE_LINE
                    )
        else:
            logger.error(
                f"Writing to interface {request.interface_id} which is not configured"
            )
        return Status(status=StatusEnum.STATUS_SUCCESS)
