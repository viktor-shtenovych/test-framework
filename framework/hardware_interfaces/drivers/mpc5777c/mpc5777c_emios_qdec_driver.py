"""! @Brief EMIOS driver for QDEC."""

#
# @file mpc5777c_emios_qdec_driver.py
#
# @section description_emios_qdec_driver Description
# This module represents the EMIOS driver for QDEC.
#
# @section libraries_emios_qdec_driver Libraries/Modules
# - grpc standard library (https://grpc.io/docs/languages/python/)
# - EmiosQdecDriverServicer module (local)
#   - Access to EmiosQdecDriverServicer class.
#
# @section notes_emios_qdec_driver Notes
# - None.
#
# @section todo_emios_qdec_driver TODO
# - None.
#
# @section author_emios_qdec_driver Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 14/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.
from typing import Any, Dict, Tuple

from typing_extensions import Optional

from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    TInterruptCallback,
)
from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_emios_common_driver import (
    EmiosCommonDriver,
)
from framework.hardware_interfaces.protoc.mpc5777c.emios_common_pb2 import (
    EmiosInputFilterType,
)
from framework.hardware_interfaces.protoc.mpc5777c.emios_qdec_driver_pb2 import (
    EmiosQdecParams,
    EmiosQdecTargetParams,
)
from framework.hardware_interfaces.protoc.mpc5777c.emios_qdec_driver_pb2_grpc import (
    EmiosQdecDriverServicer,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.support.reports import rpc_call, logger


class BaseEmiosQdecDevice:
    """
    ! Emios device implementation to simulate initialization and data interaction.
    """

    def __init__(self, group_id: int, channel: int) -> None:
        self.channel: int = channel
        self.emios_group: int = group_id
        self.mode: int | None = None
        self.filter_en: bool = False
        self.filter_input: Optional[EmiosInputFilterType] = None
        self.aux_chan_polarity: int | None = None
        self.chan_polarity: int | None = None
        self.initialized = False
        self.irq_id: int | None = None
        self.target: int | None = None

    def initialize(
        self,
        params: EmiosQdecParams,
    ) -> None:
        """
        ! Initialize the device.
        """
        self.mode = params.mode
        self.filter_en = params.filter_en
        self.filter_input = params.filter_input
        self.aux_chan_polarity = params.aux_chan_polarity
        self.chan_polarity = params.chan_polarity
        logger.info(f"Initializing Emios device with instance ID: {self.channel}")
        self.initialized = True
        self.irq_id = params.irq_id

    def reset(self) -> None:
        """
        ! Reset the device.
        """
        logger.info(
            f"Resetting eMIOS QDEC device with instance id: {self.channel} and group id: {self.emios_group}"
        )
        self.initialized = False

    def set_target(self, target: int) -> None:
        """
        ! Set the target value.
        """
        self.target = target
        logger.debug(
            f"Setting target value for eMIOS QDEC device with instance ID: {self.channel}"
        )


class EmiosQdecDriver(EmiosQdecDriverServicer, EmiosCommonDriver):
    """
    ! EMIOS driver for QDEC.
    """

    def __init__(self, raise_interrupt_func: TInterruptCallback | None) -> None:
        super().__init__(raise_interrupt_func)
        self.emios_devices: Dict[Tuple[int, int], BaseEmiosQdecDevice] = {}

    def register_device(self, device: BaseEmiosQdecDevice) -> None:
        """
        ! Register an Emios device.
        """
        key = (device.emios_group, device.channel)
        if key not in self.emios_devices:
            self.emios_devices[device.emios_group, device.channel] = device

    def wait_for_initialization(self) -> None:
        """
        ! Wait for driver initialization.
        """
        logger.debug(f"Waiting for {self.__class__.__name__} initialization.")
        self._ready.wait(0.01)
        logger.info(f"{self.__class__.__name__} initialized.")

    def get_device(self, emios_group: int, channel: int) -> BaseEmiosQdecDevice:
        """
        ! Get the device by group and channel.
        """
        key = (emios_group, channel)
        if key in self.emios_devices:
            return self.emios_devices[key]
        raise ValueError(
            f"EmiosQdecDevice with group {emios_group}, channel {channel} not found."
        )

    @rpc_call
    def EMIOS_DRV_QDEC_Init_and_Reset(
        self, request: EmiosQdecParams, context: Any
    ) -> Status:
        """
        ! Initialize and reset the EMIOS device.
        """
        channel = request.channel
        group_id = request.emios_group
        logger.debug(f"EMIOS_DRV_QDEC_Init_and_Reset called for instance: {channel}")

        if (group_id, channel) not in self.emios_devices:
            device = BaseEmiosQdecDevice(group_id, channel)
            self.register_device(device)
        else:
            device = self.get_device(group_id, channel)
        device.initialize(request)
        device.reset()
        logger.info(f"Emios QDEC device {channel} initialized and reset.")
        self._ready.set()
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def EMIOS_DRV_QDEC_SetTarget(
        self, request: EmiosQdecTargetParams, context: Any
    ) -> Status:
        """
        ! Set the target for the EMIOS device.
        """
        channel = request.channel
        group_id = request.emios_group
        target = request.target

        logger.debug(
            f"EMIOS_DRV_QDEC_SetTarget called for instance: {channel}, target: {target}"
        )

        try:
            device = self.get_device(group_id, channel)
            device.set_target(target)
            return Status(status=StatusEnum.STATUS_SUCCESS)
        except ValueError as e:
            logger.error(f"Failed to set target: {e}")
            return Status(status=StatusEnum.STATUS_FAILURE)
