from framework.hardware_interfaces.drivers.common.definitions.interfaces import Pins
from framework.hardware_interfaces.drivers.common.definitions.pins_def import OutputPins
from framework.hardware_interfaces.drivers.common.definitions.pins_def import InputPins
from framework.core.components.button import Button
from framework.core.peripherals.digital_pin import DigitalOutput, DigitalInput


class HwBoard:
    """
    ! Represents the hardware board of the fluidics.
    """

    def __init__(self, pins_drv: Pins) -> None:
        self.eth_rst_n = DigitalOutput(pins_drv, *OutputPins.ETH_RST_N.value)
        self.fpga_rst_n = DigitalOutput(pins_drv, *OutputPins.FPGA_RST_N.value)

        self.latch_closed = DigitalInput(pins_drv, *InputPins.LATCH_CLOSED.value)
        self.latch_eject = Button(pins_drv, *InputPins.LATCH_EJECT.value, False)
