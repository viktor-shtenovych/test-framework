from typing import Any, Dict, Tuple

from framework.support.reports import rpc_call, logger
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    FtmChannelABC,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.hardware_interfaces.protoc.s32k148.ftm_ic_driver_pb2 import (
    FtmIcInitParams,
    FtmIcHandle,
)
from framework.hardware_interfaces.protoc.s32k148.ftm_ic_driver_pb2_grpc import (
    FtmIcDriverServicer,
)


class FtmDriver(FtmIcDriverServicer):
    """Support for CAN bus access + stub for FootSwitch CAN driver."""

    def __init__(self) -> None:
        self.ftm: Dict[Tuple[int, int], FtmChannelABC] = {}

    def register_ftm_channel(self, channel: FtmChannelABC) -> None:
        """
        Register an FTM channel.

        Args:
            channel: The FTM channel to register.
        """
        channel_key = (channel.instance, channel.channel)
        if channel_key in self.ftm:
            raise ValueError(f"{channel_key} FTM channel already registered")

        self.ftm[channel_key] = channel

    @rpc_call
    def FtmIc_DRV_Init(self, request: FtmIcInitParams, context: Any) -> Status:
        """
        Initializes the FTM driver.

        Args:
            request: The FTM initialization parameters.
            context: The context.
        """
        channel_key = (request.instance, request.channel)
        if channel_key in self.ftm:
            self.ftm[channel_key].irq_id = request.irq_id
        else:
            logger.error(f"No FTM channel registered for {channel_key}")
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def FtmIc_DRV_Start(self, request: FtmIcHandle, context: Any) -> Status:
        """
        Starts the FTM driver.
        """
        self.ftm[(request.instance, request.channel)].start()
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def FtmIc_DRV_Stop(self, request: FtmIcHandle, context: Any) -> Status:
        """
        Stops the FTM driver.
        """
        self.ftm[(request.instance, request.channel)].stop()
        return Status(status=StatusEnum.STATUS_SUCCESS)
