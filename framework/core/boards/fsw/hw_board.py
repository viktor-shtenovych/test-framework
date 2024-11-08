from framework.hardware_interfaces.drivers.s32k148.adc_driver import AdcDriver
from framework.hardware_interfaces.drivers.common.definitions.interfaces import Pins
from framework.hardware_interfaces.drivers.common.definitions.pins_def import OutputPins
from framework.hardware_interfaces.drivers.common.definitions.pins_def import InputPins
from framework.core.components.button import Button
from framework.core.peripherals.digital_pin import DigitalOutput, DigitalInput


class HwBoard:
    """Represents the hardware board of the footswitch."""

    def __init__(self, adc_driver: AdcDriver, pins_drv: Pins) -> None:
        self.board_id = adc_driver.get_channel(1, 6)
        self.board_id.multiplier = 1.0
        self.board_id.voltage = 1.13  # FTSW CAT board ID

        self.board_version_id = adc_driver.get_channel(1, 4)
        self.board_version_id.multiplier = 1.0
        self.board_version_id.voltage = 0.682  # version 5

        self.supply_33_v = adc_driver.get_channel(0, 1)
        self.supply_33_v.multiplier = 0.5
        self.supply_33_v.voltage = 3.3
        self.supply_50_v = adc_driver.get_channel(0, 0)
        self.supply_50_v.multiplier = 0.5
        self.supply_50_v.voltage = 5.0

        self.cable_voltage = adc_driver.get_channel(0, 4)
        self.cable_voltage.multiplier = 0.1

        self.detent_temp = adc_driver.get_channel(0, 12)
        self.detent_temp.multiplier = 1

        self.detent_current = adc_driver.get_channel(0, 9)
        self.detent_current.multiplier = 0.5

        self.detent_en = DigitalOutput(pins_drv, *OutputPins.DETENT_EN.value)

        self.pd_shroud_up1 = DigitalInput(pins_drv, *InputPins.PD_SHROUD_UP1.value)
        self.pled_shdup_en1 = DigitalOutput(pins_drv, *OutputPins.PLED_SHDUP_EN1.value)
        self.pd_shroud_up2 = DigitalInput(pins_drv, *InputPins.PD_SHROUD_UP2.value)
        self.pled_shdup_en2 = DigitalOutput(pins_drv, *OutputPins.PLED_SHDUP_EN2.value)

        self.bl654_busy = DigitalInput(pins_drv, *InputPins.BL654_BUSY.value)
        self.bl654_ready_n = DigitalInput(pins_drv, *InputPins.BL654_READY_N.value)
        self.bl654_tx = DigitalInput(pins_drv, *InputPins.BL654_TX.value)

        self.vchgdt = DigitalInput(pins_drv, *InputPins.VCHGDT.value)
        self.vcoil_pg = DigitalInput(pins_drv, *InputPins.VCOIL_PG.value)
        self.coil_mon = DigitalInput(pins_drv, *InputPins.COIL_MON.value)

        self.right_vertical = Button(pins_drv, *InputPins.RIGHT_VERTICAL.value, True)
        self.right_horizontal = Button(
            pins_drv, *InputPins.RIGHT_HORIZONTAL.value, True
        )
        self.left_vertical = Button(pins_drv, *InputPins.LEFT_VERTICAL.value, True)
        self.left_horizontal = Button(pins_drv, *InputPins.LEFT_HORIZONTAL.value, True)

        self.right_heel = Button(pins_drv, *InputPins.RIGHT_HEEL.value, True)
        self.left_heel = Button(pins_drv, *InputPins.LEFT_HEEL.value, True)

        self.up_switch_0 = Button(pins_drv, *InputPins.TREADLE_UP0.value)
        self.up_switch_1 = Button(pins_drv, *InputPins.TREADLE_UP1.value)
        self.up_switch_2 = Button(pins_drv, *InputPins.TREADLE_UP2.value)
        self.up_switch_3 = Button(pins_drv, *InputPins.TREADLE_UP3.value)
        self.up_switch_4 = Button(pins_drv, *InputPins.TREADLE_UP4.value)

        self.broken_spring = DigitalInput(pins_drv, *InputPins.BROKEN_SPR.value, True)

        self.cable_in = DigitalInput(pins_drv, *InputPins.CABLE_IN.value)
