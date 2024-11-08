"""! @brief Defines module of FlacsLgsSimulator."""
##
# @file flacs_lgs_simulator.py
#
# @brief Defines module of FlacsLgsSimulator.
#
# @section description_flacs_lgs_simulator Description
# This module represents the FlacsLgsSimulator class that initializes all the hardware drivers and gRPC server.
#
# @section libraries_fflacs_lgs_simulator Libraries/Modules
# - pit module (local)
#   - Access to PITChannelManager class.
# - base_simulator module (local)
#   - Access to BaseSimulator class.
# - vtime module (local)
#   - Access to VirtualTimeWorker class.

from typing import cast

from framework.core.boards.flu.hw_board import HwBoard
from framework.core.control.pit import PITChannelManager
from framework.hardware_interfaces.drivers.common.definitions.interrupt_mapper import (
    initialize_irq_mapper,
)
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
from framework.support.reports import (
    logger,
    configure_logger_for_script,
    register_virtual_time_func,
)
from framework.hardware_interfaces.drivers import (
    get_pit_drv,
    get_pins_drv,
    get_sync_drv,
    get_async_drv,
)

from framework.hardware_interfaces.protoc.mpc5777c.pit_driver_pb2_grpc import (
    add_PitDriverServicer_to_server,
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

from framework.hardware_interfaces.drivers.common.definitions.mcu_types import MCUType
from framework.core.devices.universal_chip import UniversalChip
from framework.support.vtime import vtime_manager
from framework.support.vtime import VirtualTimeWorker


class FlacsLgsSimulator(BaseSimulator):
    """! FlacsLgsSimulator class that initializes all the hardware drivers and gRPC server."""

    MCU_TYPE: MCUType = MCUType.MPC5777C

    def __init__(self, rpc_listening_port: int) -> None:
        # Initialize interrupt mapper for the MCU type (used by logger)
        initialize_irq_mapper(self.MCU_TYPE)

        super().__init__(rpc_listening_port)

        # HW drivers simulators
        self.pins = get_pins_drv(self.irq_manager.raise_interrupt, self.MCU_TYPE)
        self.pit = get_pit_drv(self.irq_manager.raise_interrupt, PITChannelManager())
        self.sync_interface = cast(
            SifDriver, get_sync_drv(self.irq_manager.raise_interrupt, self.MCU_TYPE)
        )
        self.async_interface = get_async_drv(self.irq_manager.raise_interrupt)

        # Async interface - UniversalChip
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

        # Sync device
        self._sync_device = SynchronousIfDevice(instance_id=3, address=11)
        self._sync_device_2 = SynchronousIfDevice(instance_id=0, address=39)
        self._sync_device_3 = SynchronousIfDevice(instance_id=1, address=59)
        self._sync_device_4 = SynchronousIfDevice(instance_id=2, address=79)

        # HW board
        self.hw_board = HwBoard(self.pins)

        # Register sync interface
        self.sync_interface.register_device(self._sync_device)
        self.sync_interface.register_device(self._sync_device_2)
        self.sync_interface.register_device(self._sync_device_3)
        self.sync_interface.register_device(self._sync_device_4)

        # Register HW drivers to gRPC server
        add_PinsDriverServicer_to_server(self.pins, self.server)  # type: ignore
        add_ConnectServicer_to_server(self.rpc_connect_svc, self.server)  # type: ignore
        add_InterruptsServicer_to_server(self.irq_manager, self.server)  # type: ignore
        add_PitDriverServicer_to_server(self.pit, self.server)  # type: ignore
        add_SifDriverServicer_to_server(self.sync_interface, self.server)  # type: ignore
        add_AsyncInterfaceServicer_to_server(self.async_interface, self.server)  # type: ignore

    def wait_for_initialization(self) -> None:
        """! Wait for all the hardware drivers to initialize."""
        self.pins.wait_for_initialization()
        self.pit.wait_for_initialization()
        self.sync_interface.wait_for_initialization()
        self.async_interface.wait_for_initialization()

    def stop(self) -> None:
        """! Stop the simulator.

        This method stops the gRPC server and all the hardware drivers.
        """
        self.server.stop(5)
        self.irq_manager.stop()
        self.pit.time_manager.stop_all()
        vtime_manager.reset()


if __name__ == "__main__":
    configure_logger_for_script()
    register_virtual_time_func(vtime_manager.time_ms)

    logger.info("Starting simulator")
    sim = FlacsLgsSimulator(50051)
    sim.run()

    def _initialize() -> None:
        sim.wait_for_initialization()

    worker = VirtualTimeWorker(target=_initialize, daemon=True)
    worker.run()
    sim.server.wait_for_termination()
