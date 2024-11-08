"""! @Brief ETPU I2C driver implementation for initializing, transmitting, and receiving data."""

#
# @file etpu_i2c_driver.py
#
# @section description_etpu_i2c_driver Description
# This module represents the ETPU I2C driver implementation for initializing, transmitting, and receiving data.
#
# @section libraries_etpu_i2c_driver Libraries/Modules
# - grpc standard library (https://grpc.io/docs/languages/python/)
# - EtpuI2cDriverServicer module (local)
#   - Access to EtpuI2cDriverServicer class.
#
# @section notes_etpu_i2c_driver Notes
# - None.
#
# @section todo_etpu_i2c_driver TODO
# - None.
#
# @section author_etpu_i2c_driver Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 15/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.
from typing import Any, Dict, Callable
from framework.hardware_interfaces.drivers.common.definitions.interrupt_mapper import (
    irq_mapper,
)
from framework.hardware_interfaces.protoc.common.common_pb2 import Status, StatusEnum
from framework.hardware_interfaces.protoc.mpc5777c.etpu_i2c_driver_pb2 import (
    EtpuI2cInitParams,
    EtpuI2cTransmitParams,
    EtpuI2cReceiveReqParams,
    EtpuI2cInterfaceIdParams,
    EtpuI2cGetReceivedDataReturn,
)
from framework.hardware_interfaces.protoc.mpc5777c.etpu_i2c_driver_pb2_grpc import (
    EtpuI2cDriverServicer,
)
from framework.support.reports import rpc_call, logger
from framework.support.vtime import TimeEvent


class EtpuI2cDevice:
    """
    ! EtpuI2c device implementation to simulate initialization and data interaction.
    """

    def __init__(self, instance_id: int, address: int) -> None:
        self.instance_id = instance_id
        self.device_address = address
        self.irq_id: int = 0
        self.initialized = False
        self.data = bytearray()

    def initialize(self, irq_id: int) -> None:
        """
        ! Initialize the device.
        """
        self.irq_id = irq_id
        logger.info(f"Initializing EtpuI2c device with instance ID: {self.instance_id}")
        self.initialized = True

    def reset(self) -> None:
        """
        ! Reset the device.
        """
        logger.info(f"Resetting EtpuI2c device with instance ID: {self.instance_id}")
        self.initialized = False

    def transmit(self, message: bytes) -> None:
        """
        ! Simulate message transmission.
        """
        logger.info(
            f"Transmitting message to EtpuI2c device {self.instance_id}: {message!r}"
        )
        self.data.extend(message)

    def receive(self, size: int = 0) -> bytes:
        """
        ! Simulate receiving data from the device.
        """
        if len(self.data) < size:
            logger.warning(
                f"Requested {size} bytes, but only {len(self.data)} available."
            )
            size = len(self.data)
        self.data = self.data[size:]
        logger.info(
            f"Received {size} bytes from EtpuI2c device {self.instance_id}: {self.data}"
        )
        return self.data


class EtpuI2cDriver(EtpuI2cDriverServicer):
    """
    ! ETPU I2C driver implementation for initializing, transmitting, and receiving data.
    """

    def __init__(self, raise_interrupt_func: Callable[[int, int], None]) -> None:
        self._i2c_devices: Dict[int, EtpuI2cDevice] = {}
        self._ready = TimeEvent()
        self._raise_interrupt = raise_interrupt_func

    def register_device(self, device: EtpuI2cDevice) -> None:
        """
        ! Register an I2C device.
        """
        if device.instance_id not in self._i2c_devices:
            self._i2c_devices[device.instance_id] = device

    def wait_for_initialization(self) -> None:
        """
        ! Wait for driver initialization.
        """
        logger.debug(f"Waiting for {self.__class__.__name__} initialization.")
        self._ready.wait(0.01)
        logger.info(f"{self.__class__.__name__} initialized.")

    @rpc_call
    def ETPU_I2C_DRV_Init(self, request: EtpuI2cInitParams, context: Any) -> Status:
        """
        ! Initialize the I2C device.
        """
        instance_id = request.instance_id
        logger.info(
            f"ETPU_I2C_DRV_Init called for instance: {instance_id}: {irq_mapper(request.irq_id)}"
        )

        if instance_id not in self._i2c_devices:
            logger.error(f"EtpuI2c device with instance {instance_id} not found.")
            return Status(status=StatusEnum.STATUS_ERROR)

        device = self._i2c_devices[instance_id]
        device.initialize(request.irq_id)

        logger.info(f"EtpuI2c device {instance_id} initialized.")
        self._ready.set()
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def ETPU_I2C_DRV_Transmit(
        self, request: EtpuI2cTransmitParams, context: Any
    ) -> Status:
        """
        ! Transmit data to the I2C device.
        """
        instance_id = request.instance_id
        logger.debug(
            f"ETPU_I2C_DRV_Transmit called for instance: {instance_id}, message: {request.message!r}"
        )

        if instance_id not in self._i2c_devices:
            logger.error(f"EtpuI2c device with instance {instance_id} not found.")
            return Status(status=StatusEnum.STATUS_ERROR)

        device = self._i2c_devices[instance_id]
        device.transmit(request.message)

        logger.info(f"EtpuI2c device {instance_id} transmitted message.")
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def ETPU_I2C_DRV_ReceiveReq(
        self, request: EtpuI2cReceiveReqParams, context: Any
    ) -> Status:
        """
        ! Send a receive request to the I2C device.
        """
        instance_id = request.instance_id
        device_address = request.device_address
        size = request.size
        logger.info(
            f"ETPU_I2C_DRV_ReceiveReq called for instance: {instance_id}, size: {size}"
        )
        logger.info(
            f"ETPU_I2C_DRV_ReceiveReq called for device address: {device_address}"
        )
        if instance_id not in self._i2c_devices:
            logger.error(f"EtpuI2c device with instance {instance_id} not found.")
            return Status(status=StatusEnum.STATUS_ERROR)

        # Simulate the action of requesting data from the I2C device.
        self._raise_interrupt(self._i2c_devices[instance_id].irq_id, 0)
        logger.info(
            f"Receive request sent to EtpuI2c device {instance_id} for {request.size} bytes."
        )
        return Status(status=StatusEnum.STATUS_SUCCESS)

    @rpc_call
    def ETPU_I2C_DRV_GetReceivedData(
        self, request: EtpuI2cInterfaceIdParams, context: Any
    ) -> Any:
        """
        ! Retrieve the received data from the I2C device.
        """
        instance_id = request.instance_id
        logger.info(f"ETPU_I2C_DRV_GetReceivedData called for instance: {instance_id}")

        if instance_id not in self._i2c_devices:
            logger.error(f"EtpuI2c device with instance {instance_id} not found.")
            return Status(status=StatusEnum.STATUS_ERROR)

        device = self._i2c_devices[instance_id]
        received_data = device.receive()

        logger.info(
            f"Data received from EtpuI2c device {instance_id}: {received_data!r}"
        )

        # Ensure received_data is of type 'bytes', converting if necessary
        if isinstance(received_data, bytearray):
            received_data = bytes(received_data)

        return EtpuI2cGetReceivedDataReturn(
            status=Status(status=StatusEnum.STATUS_SUCCESS), message=received_data
        )
