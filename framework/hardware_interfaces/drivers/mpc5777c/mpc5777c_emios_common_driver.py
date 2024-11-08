"""! @Brief EMIOS Common driver for initializing and setting prescaler values."""

#
# @file framework/hardware_interfaces/drivers/mpc5777c/mpc5777c_emios_common_driver.py
#
# @section description_emios_common_driver Description
# EMIOS Common driver for initializing and setting prescaler values.
#
# @section libraries_emios_common_driver Libraries/Modules
# - grpc standard library (https://grpc.io/docs/languages/python/)
# - EmiosCommonServicer module (local)
#   - Access to EmiosCommonServicer class.
#
# @section notes_emios_common_driver Notes
# - None.
# @section todo_emios_common_driver TODO
# - None.
#
# @section author_emios_common_driver Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 24/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.
from typing import Any, Dict

from framework.hardware_interfaces.drivers.common.definitions.interrupt_mapper import (
    irq_mapper,
)
from framework.hardware_interfaces.protoc.mpc5777c.emios_common_pb2 import (
    EmiosInitGlobalParams,
    EmiosSetPrescalerEnParams,
)
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    TInterruptCallback,
)

from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.hardware_interfaces.protoc.mpc5777c.emios_common_pb2_grpc import (
    EmiosCommonServicer,
)
from framework.support.reports import rpc_call, logger
from framework.support.vtime import TimeEvent

emios_groups: Dict[int, "BaseEmiosCommonDevice"] = {}


class BaseEmiosCommonDevice:
    """
    ! Base EMIOS Common device for initialization and data interaction.
    """

    def __init__(self, emios_group: int, irq_id: int) -> None:
        self.emios_group = emios_group
        self.allow_debug_mode: bool = False
        self.low_power_mode: bool = False
        self.clk_div_val: int = 0
        self.enable_global_prescaler: bool = False
        self.enable_global_time_base: bool = False
        self.enable_external_time_base: bool = False
        self.server_time_slot: int | None = None
        self.irq_id: int = irq_id
        self.initialized = False

    def initialize(
        self,
        params: EmiosInitGlobalParams,
        _raise_interrupt_callback: TInterruptCallback | None,
    ) -> None:
        """
        ! Initialize the device with the provided parameters.
        """
        self.allow_debug_mode = params.allow_debug_mode
        self.low_power_mode = params.low_power_mode
        self.clk_div_val = params.clk_div_val
        self.enable_global_prescaler = params.enable_global_prescaler
        self.enable_global_time_base = params.enable_global_time_base
        self.enable_external_time_base = params.enable_external_time_base
        self.server_time_slot = params.server_time_slot
        self.initialized = True

        logger.debug(
            f"EmiosCommonDevice {self.emios_group} initialized with irq_id: {irq_mapper(self.irq_id)}."
        )

    def set_prescaler(self, value: bool) -> None:
        """
        ! Set the prescaler enable/disable flag.
        """
        self.enable_global_prescaler = value


class EmiosCommonDriver(EmiosCommonServicer):
    """
    ! EMIOS Common driver for initializing and setting prescaler values.
    """

    def __init__(self, raise_interrupt_func: TInterruptCallback | None) -> None:
        self._ready = TimeEvent()
        self._raise_interrupt = raise_interrupt_func

    def register_group_params(self, device: BaseEmiosCommonDevice) -> None:
        """
        ! Register an EMIOS Common device.
        """
        if device.emios_group not in emios_groups:
            emios_groups[device.emios_group] = device

    def wait_for_initialization(self) -> None:
        """
        ! Wait for driver initialization.
        """
        logger.debug(f"Waiting for {self.__class__.__name__} initialization.")
        self._ready.wait(0.01)
        logger.info(f"{self.__class__.__name__} initialized.")

    def get_group_params(self, emios_group: int) -> BaseEmiosCommonDevice:
        """
        ! Get the device by group and channel.
        """
        if emios_group in emios_groups:
            return emios_groups[emios_group]
        raise ValueError(f"EmiosCommonDevice with group {emios_group} not found.")

    @rpc_call
    def EMIOS_DRV_InitGlobal(
        self, request: EmiosInitGlobalParams, context: Any
    ) -> Status:
        """
        ! Initialize the EMIOS Common device with global parameters.
        """
        emios_group = request.emios_group

        logger.debug(f"EMIOS_DRV_InitGlobal called for group {emios_group}")

        if emios_group not in emios_groups:
            device = BaseEmiosCommonDevice(emios_group, request.irq_id)
            self.register_group_params(device)
        else:
            device = self.get_group_params(emios_group)
        device.initialize(request, self._raise_interrupt)

        logger.debug(f"EmiosCommonDevice {emios_group} initialized")
        self._ready.set()
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def EMIOS_DRV_SetPrescalerEnableBit(
        self, request: EmiosSetPrescalerEnParams, context: Any
    ) -> Status:
        """
        ! Set the prescaler enable bit for the EMIOS Common device.
        """
        emios_group = request.emios_group
        channel = request.channel
        value = request.value

        logger.debug(
            f"EMIOS_DRV_SetPrescalerEnableBit called for group {emios_group}, channel {channel}, value {value}"
        )

        device = emios_groups[emios_group]
        try:
            device.set_prescaler(value)
            logger.debug(f"Prescaler set to {value} for eMIOS group {emios_group}")
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except ValueError as e:
            logger.error(f"Error setting prescaler: {e}")
            return Status(status=StatusEnum.STATUS_ERROR)
