from typing import Any

from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.hardware_interfaces.protoc.common import connect_pb2
from framework.hardware_interfaces.protoc.common import connect_pb2_grpc
from framework.support.reports import logger, rpc_call

import threading


class Connect(connect_pb2_grpc.ConnectServicer):
    """
    ! A class to represent the connection between the test framework and the emulator.
    """

    def __init__(self) -> None:
        self._closed_event = threading.Event()

    def get_closed_event(self) -> threading.Event:
        """
        ! Get the closed event.

        @return The closed event.
        """
        return self._closed_event

    @rpc_call
    def HandShake(
        self, request: connect_pb2.HandShakeRequest, context: Any
    ) -> connect_pb2.HandShakeReply:
        """
        ! Handshake with the emulator.

        @param request The handshake request.
        @param context The context.
        @return The handshake reply.
        """
        self._closed_event.clear()
        return connect_pb2.HandShakeReply(
            message=f"Test framework says hello to {request.message}"
        )

    @rpc_call
    def Close(self, request: connect_pb2.CloseRequest, context: Any) -> Status:
        """
        ! Close the emulator.

        @param request The close request.
        @param context The context.
        @return The status of the close request.
        """
        self._closed_event.set()
        # If Close not requested from ATF
        if request.code != 2:
            # TODO: Implement closing request
            logger.fatal("Closing emulator not implemented")
        return Status(status=StatusEnum.STATUS_SUCCESS)
