"""! @brief Defines the LPIT driver."""
##
# @file lpit_driver.py
#
# @brief Defines the LPIT driver.
#
# @section description_lpit_driver Description
# This module representing the LpitDriver class.
#
# @section libraries_lpit_driver Libraries/Modules
# - grpc standard library (https://grpc.io/docs/languages/python/)
# - LPIT module (local)
#   - Access to LpitDriver class.
#
# @section notes_lpit_driver Notes
# - None.
#
# @section todo_lpit_driver TODO
# - None.
#
# @section author_lpit_driver Author(s)
# - Created by:
#   - Ihor Pryyma <ihor.pryyma@globallogic.com> on 15/05/2024;
# - Modified by:
#   - Lubos Kocvara <lubos.kocvara@globallogic.com> on 28/05/2024.
#   - Maksym Masalov <maksym.masalov@globallogic.com> on 27/08/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic.  All rights reserved.

from grpc import ServicerContext

from framework.support.reports import logger, rpc_call
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    TInterruptCallback,
    TimerManagerABC,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import StatusEnum, Status
from framework.hardware_interfaces.protoc.s32k148.lpit_driver_pb2 import (
    LpitHandle,
    LpitSetPeriodParams,
    LpitInitParams,
)
from framework.hardware_interfaces.protoc.s32k148.lpit_driver_pb2_grpc import (
    LpitDriverServicer,
)
from framework.support.vtime import TimeEvent


class LpitDriver(LpitDriverServicer):
    """! Class representing the LPIT driver.

    Inherits from LpitDriverServicer.
    """

    def __init__(
        self,
        raise_interrupt_callback: TInterruptCallback,
        time_manager: TimerManagerABC,
    ) -> None:
        """! The LpitDriver class initializer.

        @param raise_interrupt_callback  Callback function to raise an interrupt.
        @param time_manager  Instance of TimerManager to manage timers.
        """
        ## Callback function to raise an interrupt.
        self.raise_interrupt_callback = raise_interrupt_callback
        ## Instance of TimerManager to manage timers.
        self.manager = time_manager
        ## Instance of TimeEvent to signal readiness.
        self._ready = TimeEvent()

    @rpc_call
    def LPIT_DRV_Init(
        self, request: LpitInitParams, context: ServicerContext
    ) -> Status:
        """! Initializes the timer with a specified timer ID and IRQ ID.

        @param request  Request object containing timer ID and IRQ ID.
        @param context  Context of the service call.
        @return Status of the operation.
        """
        try:
            self.manager.create_timer(
                request.timer_id, request.irq_id, self.raise_interrupt_callback
            )
            logger.info(
                f"Timer {request.timer_id} initialized with IRQ ID {request.irq_id}"
            )
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except Exception as e:
            logger.error(f"Failed to initialize timer {request.timer_id}: {str(e)}")
            return Status(status=StatusEnum.STATUS_ERROR)

    @rpc_call
    def LPIT_DRV_Start(self, request: LpitHandle, context: ServicerContext) -> Status:
        """! Starts the timer specified by the timer ID.

        @param request  Request object containing timer ID.
        @param context  Context of the service call.
        @return Status of the operation.
        """
        try:
            self.manager.start_timer(request.timer_id)
            logger.info(f"Timer {request.timer_id} started")
            self._ready.set()
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except KeyError:
            logger.error(f"Timer {request.timer_id} not found")
            return Status(status=StatusEnum.STATUS_ERROR)
        except Exception as e:
            logger.error(f"Error starting timer {request.timer_id}: {str(e)}")
            return Status(status=StatusEnum.STATUS_ERROR)

    @rpc_call
    def LPIT_DRV_Stop(self, request: LpitHandle, context: ServicerContext) -> Status:
        """! Stops the timer specified by the timer ID.

        @param request  Request object containing timer ID.
        @param context  Context of the service call.
        @return Status of the operation.
        """
        try:
            self.manager.stop_timer(request.timer_id)
            logger.info(f"Timer {request.timer_id} stopped")
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except KeyError:
            logger.error(f"Timer {request.timer_id} not found")
            return Status(status=StatusEnum.STATUS_ERROR)
        except Exception as e:
            logger.error(f"Error stopping timer {request.timer_id}: {str(e)}")
            return Status(status=StatusEnum.STATUS_ERROR)

    @rpc_call
    def LPIT_DRV_SetPeriod(
        self, request: LpitSetPeriodParams, context: ServicerContext
    ) -> Status:
        """! Sets the period of the timer specified by the timer ID.

        If successful, it logs the operation and returns a success status. If the timer is not found, it logs an error
        and returns an error status. If any other exception occurs, it logs the error and returns an error status.

        @param request  A request object that contains the timer ID and the period to be set.
        @param context  The context of the service call.
        @return Status of the operation.
        """
        try:
            self.manager.set_timer_period(request.timer_id, request.period)
            logger.info(
                f"Set period {request.period} microseconds for timer {request.timer_id}"
            )
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except KeyError:
            logger.error(f"Timer {request.timer_id} not found")
            return Status(status=StatusEnum.STATUS_ERROR)
        except Exception as e:
            logger.error(f"Error setting period for timer {request.timer_id}: {str(e)}")
            return Status(status=StatusEnum.STATUS_ERROR)

    def wait_for_initialization(self) -> None:
        """! Waits for the initialization of the LPIT driver.

        This method logs the start of the wait, waits for the readiness signal,
        and then logs the completion of the initialization.
        """
        logger.debug(f"Wait for {self.__class__.__name__} initialization")
        self._ready.wait()
        logger.info(f"{self.__class__.__name__} initialized")
