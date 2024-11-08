from typing import Dict, Tuple

from grpc import ServicerContext

from framework.support.reports import rpc_call, logger
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    PwmChannelABC,
)
from framework.hardware_interfaces.protoc.s32k148.pwm_driver_pb2 import (
    PDInitParams,
    PDSetPeriodParams,
    PDSetDutyCycleParams,
)
from framework.hardware_interfaces.protoc.s32k148.pwm_driver_pb2_grpc import (
    PwmDriverServicer,
)


class PwmDriver(PwmDriverServicer):
    """
    A class to represent the PWM driver.

    This class is used to simulate the PWM driver.
    """

    def __init__(self) -> None:
        self.pwm: Dict[Tuple[int, int], PwmChannelABC] = {}

    def register_pwm_channel(self, channel: PwmChannelABC) -> None:
        """
        Register PWM channel.

        Args:
            channel (PwmChannelABC): The PWM channel.
        """
        channel_key = (channel.instance, channel.channel)
        if channel_key in self.pwm:
            raise ValueError(f"{channel_key} PWM channel already registered")

        self.pwm[channel_key] = channel

    @rpc_call
    def PwmDriver_InitChannel(
        self, request: PDInitParams, context: ServicerContext
    ) -> Status:
        """Initializes PWM channel."""
        channel_key = (request.instance_id, request.channel_id)
        if channel_key in self.pwm:
            self.pwm[channel_key].polarity = request.polarity
        else:
            logger.error(f"No PWM channel registered for {channel_key}")
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def PwmDriver_SetPeriod(
        self, request: PDSetPeriodParams, context: ServicerContext
    ) -> Status:
        """Sets PWM instance period."""
        for channel in self.pwm.values():
            if channel.instance == request.instance_id:
                channel.period = request.period
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def PwmDriver_SetDutyCycle(
        self, request: PDSetDutyCycleParams, context: ServicerContext
    ) -> Status:
        """Sets PWM channel duty cycle."""
        channel_key = (request.instance_id, request.channel_id)
        if channel_key in self.pwm:
            self.pwm[channel_key].duty_cycle = request.duty_cycle
        else:
            logger.error(f"No PWM channel registered for {channel_key}")
        return Status(status=StatusEnum.STATUS_SUCCESS)
