from framework.hardware_interfaces.drivers.s32k148.adc_driver import AdcDriver
from framework.hardware_interfaces.drivers.common.definitions.interfaces import Pins
from framework.hardware_interfaces.drivers.common.definitions.pins_def import OutputPins
from framework.core.peripherals.digital_pin import DigitalOutput
from framework.core.devices.battery_pack_manager_bq40z50 import (
    BatteryPackManagerBq40z50,
)


class Batteries:
    """
    A class that implements the Batteries driver.
    """

    def __init__(
        self,
        battery1: BatteryPackManagerBq40z50,
        battery2: BatteryPackManagerBq40z50,
        adc_driver: AdcDriver,
        pins_drv: Pins,
    ):
        self.battery1 = battery1
        self.battery2 = battery2

        # battery voltages
        adc_driver.get_channel(1, 2).multiplier = 0.3329
        adc_driver.get_channel(1, 3).multiplier = 0.3329
        adc_driver.get_channel(1, 2).voltage = 8.2
        adc_driver.get_channel(1, 3).voltage = 8.2

        # Drivers enabling battery charging
        self._charging_battery1 = DigitalOutput(
            pins_drv, *OutputPins.CHARGE_BATTERY2.value
        )
        self._charging_battery2 = DigitalOutput(
            pins_drv, *OutputPins.CHARGE_BATTERY2.value
        )

    @property
    def is_charging_voltage_enabled_battery1(self) -> bool:
        """
        Check if the charging voltage is enabled for battery 1.

        Returns:
            True if the charging voltage is enabled, False otherwise.
        """
        return self._charging_battery1.state

    @property
    def is_charging_voltage_enabled_battery2(self) -> bool:
        """
        Check if the charging voltage is enabled for battery 2.

        Returns:
            True if the charging voltage is enabled, False otherwise.
        """
        return self._charging_battery2.state
