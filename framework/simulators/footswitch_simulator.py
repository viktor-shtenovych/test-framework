"""! @Brief: This script is a simulator for the footswitch device."""
#
# @file footswitch_simulator.py
#
# @brief This script is a simulator for the footswitch device.
#
# @section description_footswitch_simulator Description
# This script initializes all the hardware drivers and gRPC server.
#
# @section libraries_footswitch_simulator Libraries/Modules
# - typing standard library (https://docs.python.org/3/library/typing.html)
# - framework module (local)
#   - Access to BaseSimulator class.
#   - Access to HwBoard class.
#   - Access to AccelerometerDeviceADXL346 class.
#   - Access to LedDriverADP8866 class.
#   - Access to BatteryPackManagerBq40z50 class.
#   - Access to I2CMuxPca9540BControl class.
#   - Access to I2CMuxPcs9540BData class.
#   - Access to DacLtc2622 class.
#   - Access to MramMr25h10 class.
#   - Access to UniversalChip class.
#   - Access to AdcDriver class.
#   - Access to SynchronousIfDevice class.
#   - Access to SifDriver class.
#   - Access to Pwm class.
#   - Access to RtcDriver class.
#   - Access to FtmDriver class.
#   - Access to get_pins_drv function.
#   - Access to get_lpit_drv function.
#   - Access to get_sync_drv function.
#   - Access to get_ftm_drv function.
#   - Access to get_pwm_drv function.
#   - Access to get_rtc_drv function.
#   - Access to get_async_drv function.
#   - Access to vtime_manager module.
#   - Access to VirtualTimeWorker class.
#   - Access to register_virtual_time_func function.
#   - Access to logger object.
#   - Access to configure_logger_for_script function.
#   - Access to register_virtual_time_func function.
#   - Access to vtime_manager object.
#   - Access to VirtualTimeWorker class.
#   - Access to TimerManager class.
#   - Access to BaseSimulator class.
#   - Access to Pwm class.
#   - Access to cast function.
#   - Access to AdcDriver class.
#   - Access to SynchronousIfDevice class.
#   - Access to BatteryPackManagerBq40z50 class.
#   - Access to I2CMuxPca9540BControl class.
#   - Access to I2CMuxPcs9540BData class.
#   - Access to DacLtc2622 class.
#   - Access to MramMr25h10 class.
#   - Access to HwBoard class.
#   - Access to TimerManager class.
#
# @section notes_footswitch_simulator Notes
# - None.
#
# @section todo_footswitch_simulator TODO
# - None.
#
# @section author_footswitch_simulator Author(s)
# - Created by:
#   - Lubos Kocvara <lubos.kocvara@globallogic.com> on 26/04/2024.
# - Modified by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 02/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.

from typing import cast

from framework.simulators.base_simulator import BaseSimulator
from framework.core.control.pwm import Pwm
from framework.support.reports import (
    logger,
    configure_logger_for_script,
    register_virtual_time_func,
)
from framework.hardware_interfaces.drivers.common.definitions.interrupt_mapper import (
    initialize_irq_mapper,
)
from framework.hardware_interfaces.drivers import (
    get_pins_drv,
    get_lpit_drv,
    get_sync_drv,
    get_ftm_drv,
    get_pwm_drv,
    get_rtc_drv,
    get_async_drv,
    get_can_bus_drv,
)
from framework.core.devices.accelerometer_device_ADXL346 import (
    AccelerometerDeviceADXL346,
)
from framework.core.devices.led_driver_adp8866 import (
    LedDriverADP8866,
)
from framework.hardware_interfaces.drivers.s32k148.adc_driver import AdcDriver
from framework.hardware_interfaces.drivers.s32k148.s32k148_sif_driver import (
    SynchronousIfDevice,
    SifDriver,
)
from framework.core.devices.battery_pack_manager_bq40z50 import (
    BatteryPackManagerBq40z50,
)
from framework.core.devices.i2c_mux_pca9540b import (
    I2CMuxPca9540BControl,
    I2CMuxPcs9540BData,
)
from framework.core.devices.dac_ltc2622 import DacLtc2622
from framework.core.devices.mram_mr25h10 import MramMr25h10
from framework.core.boards.fsw.hw_board import HwBoard
from framework.core.control.lpit import TimerManager
from framework.core.devices.universal_chip import UniversalChip

from framework.hardware_interfaces.protoc.s32k148.adc_driver_pb2_grpc import (
    add_AdcDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.common.async_interface_pb2_grpc import (
    add_AsyncInterfaceServicer_to_server,
)
from framework.hardware_interfaces.protoc.common.connect_pb2_grpc import (
    add_ConnectServicer_to_server,
)
from framework.hardware_interfaces.protoc.common.flexcan_driver_pb2_grpc import (
    add_FlexCanDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.s32k148.s32k148_pins_driver_pb2_grpc import (
    add_PinsDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.common.interrupts_pb2_grpc import (
    add_InterruptsServicer_to_server,
)
from framework.hardware_interfaces.protoc.s32k148.lpit_driver_pb2_grpc import (
    add_LpitDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.s32k148.s32k148_sif_driver_pb2_grpc import (
    add_SifDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.s32k148.ftm_ic_driver_pb2_grpc import (
    add_FtmIcDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.s32k148.pwm_driver_pb2_grpc import (
    add_PwmDriverServicer_to_server,
)
from framework.hardware_interfaces.protoc.s32k148.rtc_driver_pb2_grpc import (
    add_RtcDriverServicer_to_server,
)
from framework.hardware_interfaces.drivers.common.definitions.mcu_types import MCUType
from framework.support.vtime import vtime_manager
from framework.support.vtime import VirtualTimeWorker


class FootSwitchSimulator(BaseSimulator):
    """
    ! FootswitchSimulator class that initializes all the hardware drivers and gRPC server.
    """

    MCU_TYPE: MCUType = MCUType.S32K148

    def __init__(self, rpc_listening_port: int) -> None:
        # Initialize interrupt mapper for the MCU type (used by logger)
        initialize_irq_mapper(self.MCU_TYPE)

        super().__init__(rpc_listening_port)

        # HW drivers simulator
        self.can_node = get_can_bus_drv(self.irq_manager.raise_interrupt)
        self.pins = get_pins_drv(self.irq_manager.raise_interrupt, self.MCU_TYPE)
        self.lpit = get_lpit_drv(self.irq_manager.raise_interrupt, TimerManager())
        self.async_interface = get_async_drv(self.irq_manager.raise_interrupt)
        # fmt: off
        self.async_interface.register_stream(
            1, UniversalChip({
                # Set Radio Disable -> Response ACK
                bytes([0x55, 0x06, 0x17, 0x00, 0x72, 0xAA]):
                    bytes([0x55, 0x05, 0x97, 0xF1, 0xAA]),
                # Query FW Version -> Response Version 0.0.1.1.1
                bytes([0x55, 0x05, 0x01, 0x5B, 0xAA]):
                    bytes([0x55, 0x0A, 0x81, 0x00, 0x00, 0x01, 0x01, 0x01, 0xE3, 0xAA]),
                # Set Basic RF Settings -> Response ACK
                bytes([
                    0x55, 0x17, 0x10, 0x00, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x0C, 0x0E, 0x00, 0x00, 0x00, 0x00, 0x9A, 0xAA
                ]):
                    bytes([0x55, 0x05, 0x90, 0xEA, 0xAA]),
            },
                default_response=bytes([0x55, 0x07, 0xFF, 0x00, 0x01, 0x5C, 0xAA]))
        )
        # fmt: on
        self.adc_driver = AdcDriver(self.irq_manager.raise_interrupt)
        self.fmt_driver = get_ftm_drv()
        self.fmt_driver.register_ftm_channel(self.encoder.channel)

        self.pwm1 = Pwm(instance=5, channel=0)
        self.pwm2 = Pwm(instance=5, channel=1)
        self.pwm_driver = get_pwm_drv()
        self.pwm_driver.register_pwm_channel(self.pwm1)
        self.pwm_driver.register_pwm_channel(self.pwm2)

        self.rtc_driver = get_rtc_drv(self.irq_manager.raise_interrupt)

        self.sync_interface = cast(
            SifDriver, get_sync_drv(self.irq_manager.raise_interrupt, self.MCU_TYPE)
        )
        self.led_driver_adp8866 = LedDriverADP8866(instance_id=65536, address=39)
        self._sif_device2 = SynchronousIfDevice(instance_id=65537, address=0)
        self.accelerometer_adxl346 = AccelerometerDeviceADXL346(
            instance_id=0, address=1
        )
        self.motor_dac = DacLtc2622(instance_id=0, address=0, ref_mv=3300)
        self.mram = MramMr25h10(instance_id=2, address=0)
        # Manufacturing Information Record
        # fmt: off
        self.mram.write_to_memory(
            0x0000,  # Address
            bytes([  # Data
                0x40, 0x00, 0x00, 0x00,  # Record Size == 64
                0x00, 0x00, 0x10, 0x00,  # MRAM size in bits == 1048576 (1 Mbit)
                0x01,  # Schema Major Version == 1
                0x00,  # Schema Minor Version == 0
                0x01,  # HW - SW Compatibility Major == 1
                0x00,  # HW - SW Compatibility Minor == 0
                0x70, 0x61, 0x72, 0x74, 0x5F, 0x6E, 0x75, 0x6D,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # HW Part Num ("part_num")
                0x73, 0x65, 0x72, 0x5F, 0x6E, 0x75, 0x6D, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00,  # HW Serial Num ("ser_num")
                0x72, 0x31, 0x00, 0x00, 0x00,  # HW Revision ("r1") - 5 bytes (in code, in doc - 4)
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # Unused (8 bytes)
                0xF4, 0x0E  # CRC 16 bit CCITT
            ])
        )
        # Read Only Data
        self.mram.write_to_memory(
            0x0400,  # Address
            bytes([  # Data
                0x40, 0x00, 0x00, 0x00,  # Record Size == 64
                0x01,  # Schema Major Version == 1
                0x00,  # Schema Minor Version == 0
                0xAA,  # Owner ID == 170
                0x00,  # Unused
                0x01, 0x02,  # FSW Network ID
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,  # Unused (52 bytes)
                0xBD, 0xC6  # CRC 16 bit CCITT
            ])
        )
        # fmt: on
        self.battery1 = BatteryPackManagerBq40z50(instance_id=65537, address=11)
        self.battery2 = BatteryPackManagerBq40z50(instance_id=65537, address=11)
        self.battery_multiplexer = I2CMuxPcs9540BData(
            instance_id=65537,
            address=11,
            device1=self.battery1,
            device2=self.battery2,
        )
        self.battery_pack = I2CMuxPca9540BControl(
            instance_id=65537, address=112, mux=self.battery_multiplexer
        )
        self.sync_interface.register_device(self.led_driver_adp8866)
        self.sync_interface.register_device(self._sif_device2)
        self.sync_interface.register_device(self.accelerometer_adxl346)
        self.sync_interface.register_device(self.motor_dac)
        self.sync_interface.register_device(self.mram)
        self.sync_interface.register_device(self.battery_multiplexer)
        self.sync_interface.register_device(self.battery_pack)

        self.hw_board = HwBoard(self.adc_driver, self.pins)

        # Register HW drivers to gRPC server
        add_FlexCanDriverServicer_to_server(self.can_node, self.server)  # type: ignore
        add_PinsDriverServicer_to_server(self.pins, self.server)  # type: ignore
        add_ConnectServicer_to_server(self.rpc_connect_svc, self.server)  # type: ignore
        add_InterruptsServicer_to_server(self.irq_manager, self.server)  # type: ignore
        add_AsyncInterfaceServicer_to_server(self.async_interface, self.server)  # type: ignore
        add_AdcDriverServicer_to_server(self.adc_driver, self.server)  # type: ignore
        add_LpitDriverServicer_to_server(self.lpit, self.server)  # type: ignore
        add_SifDriverServicer_to_server(self.sync_interface, self.server)  # type: ignore
        add_FtmIcDriverServicer_to_server(self.fmt_driver, self.server)  # type: ignore
        add_PwmDriverServicer_to_server(self.pwm_driver, self.server)  # type: ignore
        add_RtcDriverServicer_to_server(self.rtc_driver, self.server)  # type: ignore

    def wait_for_initialization(self) -> None:
        """
        ! Wait for all the hardware drivers to initialize.
        """
        self.pins.wait_for_initialization()
        self.lpit.wait_for_initialization()
        self.async_interface.wait_for_initialization()
        self.adc_driver.wait_for_initialization()
        self.rtc_driver.wait_for_initialization()

    def stop(self) -> None:
        """
        ! Stop the simulator.

        This method stops the gRPC server and all the hardware drivers.
        """
        self.server.stop(5)
        self.irq_manager.stop()
        self.can_node.shutdown()
        self.lpit.manager.stop_all_timers()
        if self.rtc_driver.timer is not None:
            self.rtc_driver.timer.stop()
        self.encoder.channel.stop()
        vtime_manager.reset()


if __name__ == "__main__":
    configure_logger_for_script()
    register_virtual_time_func(vtime_manager.time_ms)

    logger.info("Starting simulator")
    sim = FootSwitchSimulator(50051)
    sim.run()

    def _initialize() -> None:
        sim.wait_for_initialization()
        # sim.hw_board.cable_in.pressed = True
        # sim.hw_board.broken_spring.pressed = False

    worker = VirtualTimeWorker(target=_initialize, daemon=True)
    worker.run()
    sim.server.wait_for_termination()
