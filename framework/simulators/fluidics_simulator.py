"""! @brief Defines module of FluidicsSimulator."""
##
# @file fluidics_simulator.py
#
# @brief Defines module of FluidicsSimulator.
#
# @section description_fluidics_simulator Description
# This module represents the FluidicsSimulator class that initializes all the hardware drivers and gRPC server.
#
# @section libraries_fluidics_simulator Libraries/Modules
# - pit module (local)
#   - Access to PITChannelManager class.
# - base_simulator module (local)
#   - Access to BaseSimulator class.
# - vtime module (local)
#   - Access to VirtualTimeWorker class.
#
# @section notes_fluidics_simulator Notes
# - None.
#
# @section todo_fluidics_simulator TODO
# - None.
#
# @section author_fluidics_simulator Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 10/07/2024.
# - Modified by:
#   - Maksym Masalov maksym.masalov@globallogic.com on 12/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.

from typing import cast

from framework.core.boards.flu.hw_board import HwBoard
from framework.core.control.pit import PITChannelManager
from framework.hardware_interfaces.drivers.common.definitions.interrupt_mapper import (
    initialize_irq_mapper,
)
from framework.hardware_interfaces.drivers.mpc5777c.etpu_i2c_driver import EtpuI2cDevice
from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_sif_driver import (
    SynchronousIfDevice,
    SifDriver,
)
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_sif_driver_pb2_grpc import (
    add_SifDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_pins_driver_pb2_grpc import (
    add_PinsDriverServicer_to_server,
)
from framework.simulators.base_simulator import BaseSimulator

from framework.hardware_interfaces.drivers import (
    get_pit_drv,
    get_pins_drv,
    get_sync_drv,
    get_async_drv,
    get_can_bus_drv,
    get_emios_qdec_drv,
    get_etpu_i2c_drv,
    get_emios_mc_drv,
    get_emios_common_drv,
    get_mcan_drv,
    get_eqadc_drv,
)

from framework.hardware_interfaces.protoc.mpc5777c.pit_driver_pb2_grpc import (
    add_PitDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.mpc5777c.etpu_i2c_driver_pb2_grpc import (
    add_EtpuI2cDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.mpc5777c.emios_qdec_driver_pb2_grpc import (
    add_EmiosQdecDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.mpc5777c.emios_mc_driver_pb2_grpc import (
    add_EmiosMcDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_eqadc_driver_pb2_grpc import (
    add_EqAdcDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.common.interrupts_pb2_grpc import (
    add_InterruptsServicer_to_server,
)
from framework.hardware_interfaces.protoc.common.connect_pb2_grpc import (
    add_ConnectServicer_to_server,
)
from framework.hardware_interfaces.protoc.common.async_interface_pb2_grpc import (
    add_AsyncInterfaceServicer_to_server,
)
from framework.hardware_interfaces.protoc.common.flexcan_driver_pb2_grpc import (
    add_FlexCanDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.mpc5777c.emios_common_pb2_grpc import (
    add_EmiosCommonServicer_to_server,
)
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_mcan_driver_pb2_grpc import (
    add_MCanDriverServicer_to_server,
)
from framework.hardware_interfaces.drivers.common.definitions.mcu_types import MCUType
from framework.core.devices.universal_chip import UniversalChip
from framework.support.vtime import vtime_manager


class FluidicsSimulator(BaseSimulator):
    """! FluidicsSimulator class that initializes all the hardware drivers and gRPC server."""

    MCU_TYPE: MCUType = MCUType.MPC5777C

    def __init__(self, rpc_listening_port: int) -> None:
        # Initialize interrupt mapper for the MCU type (used by logger)
        initialize_irq_mapper(self.MCU_TYPE)

        super().__init__(rpc_listening_port)

        # HW drivers simulators
        self.can_node = get_can_bus_drv(self.irq_manager.raise_interrupt)
        self.mcan_node = get_mcan_drv(self.irq_manager.raise_interrupt)
        self.pins = get_pins_drv(self.irq_manager.raise_interrupt, self.MCU_TYPE)
        self.pit = get_pit_drv(self.irq_manager.raise_interrupt, PITChannelManager())
        self.sync_interface = cast(
            SifDriver, get_sync_drv(self.irq_manager.raise_interrupt, self.MCU_TYPE)
        )
        self.async_interface = get_async_drv(self.irq_manager.raise_interrupt)

        self.emios_common = get_emios_common_drv(self.irq_manager.raise_interrupt)
        self.emios_qdec = get_emios_qdec_drv(self.irq_manager.raise_interrupt)
        self.emios_mc = get_emios_mc_drv(self.irq_manager.raise_interrupt)
        self.etpu_i2c = get_etpu_i2c_drv(self.irq_manager.raise_interrupt)
        self.eqadc = get_eqadc_drv(self.irq_manager.raise_interrupt)

        # TODO: Replace UniversalChip with real chip simulators
        self.async_interface.register_stream(
            1,
            UniversalChip(
                {
                    bytes([0x55]): bytes([0xAA]),
                    bytes([0xA1, 0x05]): bytes([0x55, 0x0A]),
                },
                default_response=bytes([0x55, 0x07, 0xFF, 0x00, 0x01, 0x5C, 0xAA]),
            ),
        )

        self.async_interface.register_stream(
            2,
            UniversalChip(
                {
                    bytes([0x55]): bytes([0xBB]),
                    bytes([0xA1, 0x06]): bytes([0x56, 0xA0]),
                },
                default_response=bytes([0x00, 0x01, 0x20, 0x34]),
            ),
        )

        self._sync_device = SynchronousIfDevice(instance_id=3, address=11)
        self._sync_device_2 = SynchronousIfDevice(instance_id=0, address=39)
        self._sync_device_3 = SynchronousIfDevice(instance_id=1, address=59)
        self._sync_device_4 = SynchronousIfDevice(instance_id=2, address=79)

        self.etpu_i2c_dummy_device_1 = EtpuI2cDevice(instance_id=0, address=85)

        self.hw_board = HwBoard(self.pins)

        self.sync_interface.register_device(self._sync_device)
        self.sync_interface.register_device(self._sync_device_2)
        self.sync_interface.register_device(self._sync_device_3)
        self.sync_interface.register_device(self._sync_device_4)

        self.etpu_i2c.register_device(self.etpu_i2c_dummy_device_1)

        # Register HW drivers to gRPC server
        add_FlexCanDriverServicer_to_server(self.can_node, self.server)  # type: ignore
        add_MCanDriverServicer_to_server(self.mcan_node, self.server)  # type: ignore
        add_PinsDriverServicer_to_server(self.pins, self.server)  # type: ignore
        add_ConnectServicer_to_server(self.rpc_connect_svc, self.server)  # type: ignore
        add_InterruptsServicer_to_server(self.irq_manager, self.server)  # type: ignore
        add_PitDriverServicer_to_server(self.pit, self.server)  # type: ignore
        add_SifDriverServicer_to_server(self.sync_interface, self.server)  # type: ignore
        add_AsyncInterfaceServicer_to_server(self.async_interface, self.server)  # type: ignore
        add_EmiosCommonServicer_to_server(self.emios_common, self.server)  # type: ignore
        add_EmiosQdecDriverServicer_to_server(self.emios_qdec, self.server)  # type: ignore
        add_EtpuI2cDriverServicer_to_server(self.etpu_i2c, self.server)  # type: ignore
        add_EmiosMcDriverServicer_to_server(self.emios_mc, self.server)  # type: ignore
        add_EqAdcDriverServicer_to_server(self.eqadc, self.server)  # type: ignore

    def wait_for_initialization(self) -> None:
        """! Wait for all the hardware drivers to initialize."""
        self.pins.wait_for_initialization()
        self.pit.wait_for_initialization()
        self.sync_interface.wait_for_initialization()
        self.async_interface.wait_for_initialization()
        self.can_node.wait_for_initialization()
        self.mcan_node.wait_for_initialization()
        self.emios_common.wait_for_initialization()
        self.emios_qdec.wait_for_initialization()
        self.etpu_i2c.wait_for_initialization()
        self.emios_mc.wait_for_initialization()

    def stop(self) -> None:
        """! Stop the simulator.

        This method stops the gRPC server and all the hardware drivers.
        """
        self.server.stop(5)
        self.irq_manager.stop()
        self.can_node.shutdown()
        self.mcan_node.shutdown()
        self.pit.time_manager.stop_all()
        self.emios_mc.stop_all()
        vtime_manager.reset()
