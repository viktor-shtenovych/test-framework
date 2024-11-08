from grpc import ServicerContext

from typing import Callable, Optional

from framework.support.reports import rpc_call, logger

from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.hardware_interfaces.protoc.s32k148.rtc_driver_pb2 import (
    RtcSetTimeParams,
    RtcHandle,
    RtcInitParams,
)
from framework.hardware_interfaces.protoc.s32k148.rtc_driver_pb2_grpc import (
    RtcDriverServicer,
)

from framework.core.control.rtc import RTC_Timer
from framework.support.vtime import TimeEvent


class RtcDriver(RtcDriverServicer):
    """
    A class that implements the RTC driver.

    Attributes:
        raise_interrupt: A function that raises an interrupt.
        timer: An instance of the RTC_Timer class.
        _ready: An event that signals that the RTC is ready.
    """

    def __init__(self, raise_interrupt_func: Callable[[int, int], None]) -> None:
        self.raise_interrupt = raise_interrupt_func
        self.timer: Optional[RTC_Timer] = None
        self._ready = TimeEvent()

    @rpc_call
    def RTC_DRV_Init(self, request: RtcInitParams, context: ServicerContext) -> Status:
        """Initializes RTC."""
        try:
            self.timer = RTC_Timer(request.seconds_irq_id, self.raise_interrupt)
            logger.info(
                f"RTC initialized with IRQ ID {request.irq_id}, Seconds IRQ ID {request.seconds_irq_id}"
            )
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except Exception as e:
            logger.error(f"Failed to initialize RTC: {str(e)}")
            return Status(status=StatusEnum.STATUS_ERROR)

    @rpc_call
    def RTC_DRV_Enable(self, request: RtcHandle, context: ServicerContext) -> Status:
        """Enables RTC."""
        try:
            if self.timer is not None:
                self.timer.start()
            self._ready.set()
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except Exception as e:
            logger.error(f"Error starting RTC: {str(e)}")
            return Status(status=StatusEnum.STATUS_ERROR)

    @rpc_call
    def RTC_DRV_Disable(self, request: RtcHandle, context: ServicerContext) -> Status:
        """Disables RTC."""
        try:
            if self.timer is not None:
                self.timer.stop()
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except Exception as e:
            logger.error(f"Error stopping RTC: {str(e)}")
            return Status(status=StatusEnum.STATUS_ERROR)

    @rpc_call
    def RTC_DRV_SetTimeSeconds(
        self, request: RtcSetTimeParams, context: ServicerContext
    ) -> Status:
        """Sets RTC time."""
        try:
            if self.timer is not None:
                self.timer.set_seconds(request.seconds)
            logger.info("RTC time was set")
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except Exception as e:
            logger.error(f"Error setting RTC time: {str(e)}")
            return Status(status=StatusEnum.STATUS_ERROR)

    def wait_for_initialization(self) -> None:
        """Wait for RTC initialization."""
        logger.debug(f"Wait for {self.__class__.__name__} initialization")
        self._ready.wait()
        logger.info(f"{self.__class__.__name__} initialized")
