"""! @brief Defines the PIT driver."""
##
# @file pit_driver.py
#
# @brief Defines the PIT driver.
#
# @section description_pit_driver Description
# This module represents the PitDriver class.
#
# @section libraries_pit_driver Libraries/Modules
# - grpc standard library (https://grpc.io/docs/languages/python/)
# - PIT module (local)
#   - Access to PitDriver class.
#
# @section notes_pit_driver Notes
# - None.
#
# @section todo_pit_driver TODO
# - None.
#
# @section author_pit_driver Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 06/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.

from grpc import ServicerContext

from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    TInterruptCallback,
)
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    PITChannelManagerABC,
)
from framework.support.reports import logger, rpc_call
from framework.hardware_interfaces.protoc.common.common_pb2 import StatusEnum, Status
from framework.hardware_interfaces.protoc.mpc5777c.pit_driver_pb2 import (
    PitChannelParams,
    PitChannelIrqParams,
    PitSetPeriodByUsParams,
)
from framework.hardware_interfaces.protoc.mpc5777c.pit_driver_pb2_grpc import (
    PitDriverServicer,
)
from framework.support.vtime import TimeEvent


class PitDriver(PitDriverServicer):
    """! Class representing the PIT driver.

    Inherits from PitDriverServicer.
    """

    def __init__(
        self,
        raise_interrupt_callback: TInterruptCallback,
        time_manager: PITChannelManagerABC,
    ) -> None:
        """! The PitDriver class initializer."""
        self._raise_interrupt_callback = raise_interrupt_callback
        self.time_manager = time_manager
        self._ready = TimeEvent()

    @rpc_call
    def PIT_DRV_StartChannel(
        self, request: PitChannelParams, context: ServicerContext
    ) -> Status:
        """! Starts the specified PIT channel.

        @param request  Request object containing instance ID and channel ID.
        @param context  Context of the service call.
        @return Status of the operation.
        """
        try:
            self.time_manager.start_channel(request.channel_id)
            logger.info(f"PIT channel {request.channel_id} started")
            self._ready.set()
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except KeyError:
            logger.error(f"Timer {request.channel_id} not found")
            return Status(status=StatusEnum.STATUS_ERROR)
        except Exception as e:
            logger.error(f"Failed to start PIT channel: {str(e)}")
            return Status(status=StatusEnum.STATUS_ERROR)

    @rpc_call
    def PIT_DRV_StopChannel(
        self, request: PitChannelParams, context: ServicerContext
    ) -> Status:
        """! Stops the specified PIT channel.

        @param request  Request object containing instance ID and channel ID.
        @param context  Context of the service call.
        @return Status of the operation.
        """
        try:
            self.time_manager.stop_channel(request.channel_id)
            logger.info(f"PIT channel {request.channel_id} stopped")
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except KeyError:
            logger.error(f"Timer {request.channel_id} not found")
            return Status(status=StatusEnum.STATUS_ERROR)
        except Exception as e:
            logger.error(f"Failed to stop PIT channel: {str(e)}")
            return Status(status=StatusEnum.STATUS_ERROR)

    @rpc_call
    def PIT_DRV_SetPeriodByUs(
        self, request: PitSetPeriodByUsParams, context: ServicerContext
    ) -> Status:
        """! Sets the timer period for the specified PIT channel in microseconds.

        @param request  Request object containing instance ID, channel ID, and period in microseconds.
        @param context  Context of the service call.
        @return Status of the operation.
        """
        try:
            self.time_manager.create_channel(request.channel_id)
            self.time_manager.set_period_us(request.channel_id, request.period_us)
            logger.info(
                f"Set period {request.period_us} us for channel {request.channel_id}"
            )
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except KeyError:
            logger.error(f"Timer {request.channel_id} not found")
            return Status(status=StatusEnum.STATUS_ERROR)
        except Exception as e:
            logger.error(f"Failed to set timer period in us: {str(e)}")
            return Status(status=StatusEnum.STATUS_ERROR)

    @rpc_call
    def PIT_DRV_EnableInterrupt(
        self, request: PitChannelIrqParams, context: ServicerContext
    ) -> Status:
        """! Enables the interrupt for the specified PIT channel.

        @param request  Request object containing instance ID, channel ID, and IRQ ID.
        @param context  Context of the service call.
        @return Status of the operation.
        """
        try:
            self.time_manager.enable_interrupt(
                request.channel_id, request.irq_id, self._raise_interrupt_callback
            )
            logger.info(f"Enabled interrupt for channel {request.channel_id}")
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except KeyError:
            logger.error(f"Timer {request.channel_id} not found")
            return Status(status=StatusEnum.STATUS_ERROR)
        except Exception as e:
            logger.error(
                f"Failed to enable interrupt for channel {request.channel_id}: {str(e)}"
            )
            return Status(status=StatusEnum.STATUS_ERROR)

    @rpc_call
    def PIT_DRV_DisableInterrupt(
        self, request: PitChannelIrqParams, context: ServicerContext
    ) -> Status:
        """! Disables the interrupt for the specified PIT channel.

        @param request  Request object containing instance ID and channel ID.
        @param context  Context of the service call.
        @return Status of the operation.
        """
        try:
            self.time_manager.disable_interrupt(request.channel_id)
            logger.info(f"Interrupt disabled for timer {request.channel_id}")
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except KeyError:
            logger.error(f"Timer {request.channel_id} not found")
            return Status(status=StatusEnum.STATUS_ERROR)
        except Exception as e:
            logger.error(
                f"Error setting period for timer {request.channel_id}: {str(e)}"
            )
            return Status(status=StatusEnum.STATUS_ERROR)

    def wait_for_initialization(self) -> None:
        """! Waits for the initialization of the PIT driver.

        This method logs the start of the wait, waits for the readiness signal,
        and then logs the completion of the initialization.
        """
        logger.debug(f"Wait for {self.__class__.__name__} initialization")
        self._ready.wait()
        logger.info(f"{self.__class__.__name__} initialized")
