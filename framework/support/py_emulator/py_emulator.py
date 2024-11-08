import time

import grpc

from framework.hardware_interfaces.drivers.common.interrupts import IrqId
from framework.hardware_interfaces.drivers.common.definitions.pins_def import (
    Ports,
    InputPins,
    OutputPins,
)
from framework.hardware_interfaces.protoc.common.connect_pb2 import HandShakeRequest
from framework.hardware_interfaces.protoc.common.connect_pb2_grpc import ConnectStub
from framework.hardware_interfaces.protoc.common.flexcan_driver_pb2 import FCInitParams
from framework.support.reports import (
    configure_logger_for_script,
    logger,
    register_virtual_time_func,
)
from framework.hardware_interfaces.protoc.common.flexcan_driver_pb2_grpc import (
    FlexCanDriverStub,
)
from framework.hardware_interfaces.protoc.s32k148.s32k148_pins_driver_pb2 import (
    Direction,
    PinSettingConfig,
    PinsInitParams,
    PortIrqId,
)
from framework.hardware_interfaces.protoc.s32k148.s32k148_pins_driver_pb2_grpc import (
    PinsDriverStub,
)
from framework.support.py_emulator.py_emulator_data import (
    status_210,
    status_211_battery,
)
from framework.hardware_interfaces.protoc.common.interrupts_pb2 import IdleContext
from framework.hardware_interfaces.protoc.common.interrupts_pb2_grpc import (
    InterruptsStub,
)


class InterruptType:
    """Interrupt type."""

    pass


class DummyEmulator:
    """Mock of emulator."""

    def __init__(self) -> None:
        self.clock = 0

    def send_can_data(
        self, can_stub: FlexCanDriverStub, msg_id: int, data: bytes
    ) -> None:
        """
        Send CAN data.

        Args:
            can_stub: The CAN stub.
            msg_id: The message ID.
            data: The data.
        """
        # tx_info = DataInfo(msg_type=MsgBufIdType.STD, is_remote=False)
        # request = SendRequest(
        #     instance=1, mb_idx=2, tx_info=tx_info, msg_id=msg_id, data=data
        # )
        # response = can_stub.FLEXCAN_DRV_Send(request)
        # logger.info(f"Client received status code: {response.status}")
        pass

    def wait_for_interrupt(self, irq_stub: InterruptsStub) -> None:
        """
        Wait for interrupt.

        Args:
            irq_stub: The IRQ stub.
        """
        irq_context = irq_stub.WaitForInterrupt(IdleContext(idle_cycles=1))
        self.clock = irq_context.time * 1e-3
        logger.info(f"Interrupt received: {IrqId(irq_context.irq_id).name}")

    def run(self) -> None:
        """
        Run the emulator.
        """
        with grpc.insecure_channel("localhost:50051") as channel:
            can_stub = FlexCanDriverStub(channel)  # type: ignore
            pins_stub = PinsDriverStub(channel)  # type: ignore
            conn_stub = ConnectStub(channel)  # type: ignore
            irq_stub = InterruptsStub(channel)  # type: ignore

            conn_stub.HandShake(HandShakeRequest(message="Python emulator"))

            # Initialization
            params = FCInitParams(
                instance_id=0,
                irq_id=IrqId.MemoryManagement_IRQn,
                max_num_mb=32,
                num_id_rx_filters=8,
            )
            can_stub.FLEXCAN_DRV_Init(params)

            pins_config = [
                PinSettingConfig(
                    pin_id=pin.value[1],
                    port_id=pin.value[0],
                    direction=Direction.FSW_IN,
                    init_value=0,
                )
                for pin in InputPins
            ]
            pins_config.extend(
                [
                    PinSettingConfig(
                        pin_id=pin.value[1],
                        port_id=pin.value[0],
                        direction=Direction.FSW_OUT,
                        init_value=0,
                    )
                    for pin in OutputPins
                ]
            )
            args = PinsInitParams(
                config=pins_config,
                irq_ids=[
                    PortIrqId(port_id=Ports.PORT_E, irq_id=IrqId.MemoryManagement_IRQn)
                ],
            )
            pins_stub.PINS_DRV_Init(args)

            while True:
                try:
                    self.wait_for_interrupt(irq_stub)

                    self.send_can_data(can_stub, 0x210, status_210)
                    self.send_can_data(can_stub, 0x210, status_210)
                    self.send_can_data(can_stub, 0x211, status_211_battery)

                    for _ in range(30):
                        self.wait_for_interrupt(irq_stub)
                        self.wait_for_interrupt(irq_stub)
                        self.wait_for_interrupt(irq_stub)
                        self.wait_for_interrupt(irq_stub)

                    time.sleep(2)
                except grpc.RpcError:
                    logger.info("Connection closed")
                    break


if __name__ == "__main__":
    configure_logger_for_script()

    emulator = DummyEmulator()
    register_virtual_time_func(lambda: emulator.clock)
    logger.info("Starting dummy emulator")
    emulator.run()
