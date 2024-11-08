"""! @Brief MPC5777C EQADC driver implementation."""

#
# @file mpc5777c_eqadc_driver.py
#
# @section description_mpc5777c_eqadc_driver Description
# This module represents the MPC5777C EQADC driver implementation.
#
# @section libraries_mpc5777c_eqadc_driver Libraries/Modules
# - grpc standard library (https://grpc.io/docs/languages/python/)
# - EqAdcDriverServicer module (local)
#   - Access to EqAdcDriverServicer class.
#
# @section notes_mpc5777c_eqadc_driver Notes
# - None.
#
# @section todo_mpc5777c_eqadc_driver TODO
# - None.
#
# @section author_mpc5777c_eqadc_driver Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 31/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.
from typing import Any
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    TInterruptCallback,
)
from framework.hardware_interfaces.drivers.common.definitions.interrupt_mapper import (
    irq_mapper,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_eqadc_driver_pb2 import (
    EqAdcConfig,
    EqAdcCommand,
    EqAdcInitParams,
    EqAdcCcCalibrateConverterParams,
    EqAdcCCSamplesRequestParams,
)
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_eqadc_driver_pb2_grpc import (
    EqAdcDriverServicer,
)
from framework.support.reports import logger
from framework.support.vtime import TimeEvent
from random import randint


class BaseEqAdcDevice:
    """
    ! Base class for EQADC device driver.
    """

    def __init__(self, instance_id: int) -> None:
        self.instance_id = instance_id
        self.sample_num: int | None = None
        self.adc_config: list[EqAdcConfig] = []
        self.adc_commands: list[EqAdcCommand] = []
        self.irq_id: int = 0
        self.calibrated = False
        self.initialized = False

    def initialize(self, params: EqAdcInitParams) -> None:
        """
        ! Initialize the device with given parameters.
        """
        self.sample_num = params.samples_num
        self.adc_config = params.adc_config
        self.adc_commands = params.adc_commands
        self.irq_id = params.irq_id
        self.initialized = True
        logger.info(f"EQADC device {self.instance_id} initialized")

    def calibrate_converter(
        self, gain: int, offset: int, rais_interrupt_callback: TInterruptCallback
    ) -> None:
        """
        ! Calibrate the converter.
        """
        self.calibrated = True
        if self.adc_config is None or self.irq_id is None:
            raise ValueError(f"EQADC device {self.instance_id} not initialized")

        for idx in range(len(self.adc_config)):
            self.adc_config[idx].gain = gain
            self.adc_config[idx].offset = offset

        logger.info(
            f"EQADC device {self.instance_id} calibrated with gain {gain} and offset {offset}"
        )


class EqAdcDriver(EqAdcDriverServicer):
    """
    ! EQADC driver implementation to simulate initialization and data interaction.
    """

    def __init__(self, raise_interrupt_func: TInterruptCallback) -> None:
        self.raise_interrupt = raise_interrupt_func
        self.devices: dict[int, BaseEqAdcDevice] = {}
        self._ready = TimeEvent()

    def _initialize_device(self, request: EqAdcInitParams) -> None:
        """
        ! Helper function to initialize a new device.
        """
        instance_id = request.instance_id
        irq_id = request.irq_id
        if instance_id not in self.devices:
            self.devices[instance_id] = BaseEqAdcDevice(instance_id)
            self.devices[instance_id].initialize(request)
            logger.debug(
                f"New EQADC device {instance_id} created with IRQ {irq_mapper(irq_id)}"
            )
        else:
            logger.warning(f"EQADC device {instance_id} already initialized")

    def get_device(self, instance_id: int) -> BaseEqAdcDevice:
        """
        ! Helper function to retrieve a device.
        """
        if instance_id not in self.devices:
            raise ValueError(f"EQADC device {instance_id} not initialized")
        return self.devices[instance_id]

    def wait_for_initialization(self) -> None:
        """
        ! Wait for initialization.
        """
        logger.debug("Wait for EQADC driver initialization")
        self._ready.wait()
        logger.info(
            "EQADC driver initialized with devices: "
            + ", ".join(str(device) for device in self.devices.keys())
        )

    def EQADC_DRV_CC_Init(self, request: EqAdcInitParams, context: Any) -> Status:
        """
        ! Initialize the driver.
        """
        self._initialize_device(request)
        self._ready.set()
        return Status(status=StatusEnum.STATUS_SUCCESS)

    def EQADC_DRV_CC_CalibrateConverter(
        self, request: EqAdcCcCalibrateConverterParams, context: Any
    ) -> Status:
        """
        ! Calibrate the driver.
        """
        instance_id = request.instance_id
        device = self.get_device(instance_id)
        device.calibrate_converter(request.gain, request.offset, self.raise_interrupt)
        return Status(status=StatusEnum.STATUS_SUCCESS)

    def EQADC_DRV_CC_SamplesRequest(
        self, request: EqAdcCCSamplesRequestParams, context: Any
    ) -> Status:
        """
        ! Request samples.
        """
        for channel in request.channel_id:
            logger.debug(
                f"Requesting samples for EQADC device {request.instance_id}, channel {channel}"
            )
            self.raise_interrupt(
                self.devices[request.instance_id].irq_id,
                request.instance_id
                | channel << 2
                | request.instance_id << 24
                | channel << 16
                | randint(0, 255) << 8,
            )
        return Status(status=StatusEnum.STATUS_SUCCESS)
