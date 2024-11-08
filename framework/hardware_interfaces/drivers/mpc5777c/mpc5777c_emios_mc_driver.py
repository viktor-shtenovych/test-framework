"""! @Brief Emios MC driver implementation for initializing and setting period values."""

#
# @file mpc5777c_emios_mc_driver.py
#
# @section description_mpc5777c_emios_mc_driver Description
# This module represents the Emios MC driver implementation for initializing and setting period values.
#
# @section libraries_mpc5777c_emios_mc_driver Libraries/Modules
# - grpc standard library (https://grpc.io/docs/languages/python/)
# - EmiosMcDriverServicer module (local)
#   - Access to EmiosMcDriverServicer class.
#
# @section notes_mpc5777c_emios_mc_driver Notes
# - None.
#
# @section todo_mpc5777c_emios_mc_driver TODO
# - None.
#
# @section author_mpc5777c_emios_mc_driver Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 21/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved
from typing import Any, Dict, Tuple, Optional

from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_emios_common_driver import (
    EmiosCommonDriver,
)
from framework.hardware_interfaces.protoc.mpc5777c.emios_common_pb2 import (
    EmiosInputFilterType,
)
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    TInterruptCallback,
)
from framework.hardware_interfaces.drivers.common.definitions.emios_channel_manager import (
    EMIOSChannelManager,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.hardware_interfaces.protoc.mpc5777c.emios_mc_driver_pb2 import (
    EmiosMcInitParams,
    EmiosMcSetPeriodParams,
    EmiosMcMode,
    EmiosClockInternalPsType,
    EmiosEdgeTriggerMode,
)
from framework.hardware_interfaces.protoc.mpc5777c.emios_mc_driver_pb2_grpc import (
    EmiosMcDriverServicer,
)

from framework.support.reports import rpc_call, logger


class BaseEmiosMcDevice:
    """
    ! Emios MC device implementation to simulate initialization and data interaction.
    """

    def __init__(self, emios_group: int, channel: int) -> None:
        self.emios_group = emios_group
        self.channel = channel
        self.mode: Optional[EmiosMcMode] = None
        self.period = 0
        self.internal_prescaler: Optional[EmiosClockInternalPsType] = None
        self.internal_prescaler_en = False
        self.filter_input: Optional[EmiosInputFilterType] = None
        self.filter_en = False
        self.trigger_mode: Optional[EmiosEdgeTriggerMode] = None
        self.irq_id: int | None = None
        self.initialized = False
        self.time_manager = EMIOSChannelManager()

    def _start_channel(
        self, _raise_interrupt_callback: TInterruptCallback | None
    ) -> None:
        """
        ! Start the channel.
        """
        if self.irq_id is None:
            raise ValueError(
                f"Interrupt ID not set for EmiosMcDevice {self.emios_group}/{self.channel}"
            )
        self.time_manager.create_channel(self.emios_group, self.channel)
        self.time_manager.set_period_us(self.emios_group, self.channel, self.period)
        self.time_manager.enable_interrupt(
            self.emios_group, self.channel, self.irq_id, _raise_interrupt_callback
        )
        self.time_manager.start_channel(self.emios_group, self.channel)

    def initialize(
        self,
        params: EmiosMcInitParams,
        _raise_interrupt_callback: TInterruptCallback | None,
    ) -> None:
        """
        ! Initialize the device with given parameters.
        """
        self.mode = params.mode
        self.period = params.period
        self.internal_prescaler = params.internal_prescaler
        self.internal_prescaler_en = params.internal_prescaler_en
        self.filter_input = params.filter_input
        self.filter_en = params.filter_en
        self.trigger_mode = params.trigger_mode
        self.irq_id = params.irq_id
        self.initialized = True

        self._start_channel(_raise_interrupt_callback)
        logger.info(
            f"EmiosMcDevice {self.emios_group}/{self.channel} initialized with mode {self.mode}, period {self.period}"
        )

    def set_period(self, period: int) -> None:
        """
        ! Set the period value for the device.
        """
        if not self.initialized:
            logger.error(
                f"EmiosMcDevice {self.emios_group}/{self.channel} is not initialized."
            )
            raise ValueError("Device not initialized")

        self.period = period
        self.time_manager.set_period_us(self.emios_group, self.channel, self.period)
        logger.info(
            f"EmiosMcDevice {self.emios_group}/{self.channel} period set to {self.period}"
        )


class EmiosMcDriver(EmiosMcDriverServicer, EmiosCommonDriver):
    """
    ! Emios MC driver implementation for initializing and setting period values.
    """

    def __init__(self, raise_interrupt_func: TInterruptCallback | None) -> None:
        super().__init__(raise_interrupt_func)
        self.emios_devices: Dict[Tuple[int, int], BaseEmiosMcDevice] = {}

    def register_device(self, device: BaseEmiosMcDevice) -> None:
        """
        ! Register an Emios MC device.
        """
        key = (device.emios_group, device.channel)
        if key not in self.emios_devices:
            self.emios_devices[key] = device
            logger.info(
                f"Registered EmiosMcDevice with group {device.emios_group}, channel {device.channel}"
            )

    def stop_all(self) -> None:
        """
        ! Stop all running channels.
        """
        for device in self.emios_devices.values():
            device.time_manager.stop_channel(device.emios_group, device.channel)

    def wait_for_initialization(self) -> None:
        """
        ! Wait for driver initialization.
        """
        logger.debug(f"Waiting for {self.__class__.__name__} initialization.")
        self._ready.wait(0.01)
        logger.info(f"{self.__class__.__name__} initialized.")

    def get_device(self, emios_group: int, channel: int) -> BaseEmiosMcDevice:
        """
        ! Get the device by group and channel.
        """
        key = (emios_group, channel)
        if key in self.emios_devices:
            return self.emios_devices[key]
        raise ValueError(
            f"EmiosMcDevice with group {emios_group}, channel {channel} not found."
        )

    @rpc_call
    def EMIOS_DRV_MC_InitMode(self, request: EmiosMcInitParams, context: Any) -> Status:
        """
        ! Initialize the Emios MC device with the given parameters.
        """
        emios_group = request.emios_group
        channel = request.channel
        key = (emios_group, channel)

        logger.debug(
            f"EMIOS_DRV_MC_InitMode called for group {emios_group}, channel {channel}"
        )

        if key not in self.emios_devices:
            device = BaseEmiosMcDevice(emios_group, channel)
            self.register_device(device)
        else:
            device = self.get_device(*key)
        device.initialize(request, self._raise_interrupt)

        logger.info(
            f"EmiosMcDevice {emios_group}/{channel} initialized in mode {request.mode}"
        )
        self._ready.set()
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def EMIOS_DRV_MC_SetPeriodValue(
        self, request: EmiosMcSetPeriodParams, context: Any
    ) -> Status:
        """
        ! Set the period value for the Emios MC device.
        """
        emios_group = request.emios_group
        channel = request.channel
        period = request.period
        key = (emios_group, channel)

        logger.debug(
            f"EMIOS_DRV_MC_SetPeriodValue called for group {emios_group}, channel {channel}, period {period}"
        )

        if key not in self.emios_devices:
            logger.error(
                f"EmiosMcDevice with group {emios_group}, channel {channel} not found."
            )
            return Status(status=StatusEnum.STATUS_ERROR)

        device = self.emios_devices[key]
        try:
            device.set_period(period)
            logger.debug(
                f"Period value set to {period} for EmiosMcDevice {emios_group}/{channel}"
            )
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except ValueError as e:
            logger.error(f"Error setting period value: {e}")
            return Status(status=StatusEnum.STATUS_ERROR)
