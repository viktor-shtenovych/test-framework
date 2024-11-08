"""Battery and Charging Tests."""

from typing import cast


from framework.communications.uvcs_footswitch.msg_types.aux_data_types import (
    AuxDataType,
    BatteryStatus1,
    BatteryStatus3,
    BatteryDebugInfo,
)
from framework.communications.uvcs_footswitch.msg_types.configuration_msg import (
    ConfigurationMsg310,
)
from framework.communications.uvcs_footswitch.msg_types.msg_data_structures import (
    FootSwitchState,
)
from framework.communications.uvcs_footswitch.msg_types.real_time_status_msgs import (
    StatusMsg211,
)
from framework.apps.footswitch import FootSwitch
from framework.support.reports import report
from framework.support.reports import logger
from tests.footswitch_tests.utils import connect_footswitch_to_console


class TestBatteryCharging:
    """Battery and Charging Tests."""

    @staticmethod
    def wait_for_charging_voltage(
        foot_switch: FootSwitch, charging: bool, max_wait_time_ms: int = 4_000
    ) -> bool:
        """
        Wait for charging voltage to be present/not present for battery 1.
        """
        max_time = foot_switch.vtime.time_ms() + max_wait_time_ms
        # Wait for charging is started
        while (
            foot_switch.batteries.is_charging_voltage_enabled_battery2 is not charging
            and foot_switch.vtime.time_ms() < max_time
        ):
            foot_switch.vtime.sleep(0.01)

        logger.info(
            f"Charging voltage for battery1: {foot_switch.batteries.is_charging_voltage_enabled_battery1}"
        )
        logger.info(
            f"Charging voltage for battery2: {foot_switch.batteries.is_charging_voltage_enabled_battery2}"
        )

        # Send config message to keep CAN communication alive
        foot_switch.wired_conn.send_config(ConfigurationMsg310())

        return foot_switch.batteries.is_charging_voltage_enabled_battery1

    @staticmethod
    def wait_for_battery_status(
        foot_switch: FootSwitch, charging: bool, charging_level: int | None = None
    ) -> StatusMsg211:
        """
        Wait for battery status message.
        """
        message211 = foot_switch.wired_conn.get_status_211(
            lambda x: x.aux_type == AuxDataType.BatteryStatus1
            and x.data.charging is charging  # type: ignore
            and (x.data.level == charging_level if charging_level else True)  # type: ignore
        )
        return message211

    def test_battery_low_charging_cabled(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0147] This test verifies that the footswitch charges a battery with low charge level when cabled.
        """
        with report.TestStep(
            "Install batteries with charge level of 40% ± 5% in a Footswitch."
        ):
            foot_switch.batteries.battery1.set_charge_level(40)
            foot_switch.batteries.battery2.set_charge_level(40)

        with report.TestStep(
            "Cable Footswitch to Console and keep the treadle up. "
            "Note down “BatteryLevel” reported by “FswStatus” message"
        ) as step:
            foot_switch_state, message = connect_footswitch_to_console(
                foot_switch, beacons=None
            )
            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                foot_switch_state,
                comment=f"Status message: {message}",
            )

            self.wait_for_charging_voltage(foot_switch, charging=True)

            message211 = self.wait_for_battery_status(
                foot_switch, charging=True, charging_level=70
            )
            message211.data = cast(BatteryStatus1, message211.data)

            step.verify_equal(
                "The “IsFswCharging” as true in the “FswStatus” message view.",
                True,
                message211.data.charging,
                comment=f"Status message: {message211}, Battery level: {message211.data.level} %",
            )

            step.verify_equal(
                "The right user LED on Footswitch is blinking indicating charging.",
                foot_switch.leds.LED_MODE.ON_BLINKING,
                foot_switch.leds.get_led_mode(foot_switch.leds.LEDS.RIGHT_GREEN),
            )

        with report.TestStep("Press on the treadle."):
            foot_switch.treadle.down(1000)

            self.wait_for_charging_voltage(foot_switch, charging=False)

            message211 = self.wait_for_battery_status(
                foot_switch, charging=False, charging_level=70
            )
            message211.data = cast(BatteryStatus1, message211.data)

            step.verify_equal(
                "The right user LED is solid green indicating charging is OFF.",
                foot_switch.leds.LED_MODE.ON_SOLID,
                foot_switch.leds.get_led_mode(foot_switch.leds.LEDS.RIGHT_GREEN),
            )

        with report.TestStep(
            "Release the treadle and periodically check the setup, wait up to three hours.  "
            "Check the “BatteryLevel” displayed in the “FswStatus” message view."
        ) as step:
            foot_switch.treadle.up()

            self.wait_for_charging_voltage(foot_switch, charging=True)

            message211 = self.wait_for_battery_status(
                foot_switch, charging=True, charging_level=70
            )
            message211.data = cast(BatteryStatus1, message211.data)

            step.verify_equal(
                "The “IsFswCharging” as true in the “FswStatus” message view.",
                True,
                message211.data.charging,
                comment=f"Status message: {message211}",
            )

            # Simulate battery being charged
            logger.info("Set battery charge level to 100%")
            foot_switch.batteries.battery1.set_charge_level(100)
            foot_switch.batteries.battery2.set_charge_level(100)

            self.wait_for_charging_voltage(foot_switch, charging=False)

            message210 = foot_switch.wired_conn.get_status_210()
            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                message210.foot_switch_state,
                comment=f"Status message: {message210}",
            )

            message211 = self.wait_for_battery_status(
                foot_switch, charging=False, charging_level=100
            )
            message211.data = cast(BatteryStatus1, message211.data)

            step.verify_equal(
                "The “IsFswCharging” as false in the “FswStatus” message view.",
                False,
                message211.data.charging,
                comment=f"Status message: {message211}",
            )

            step.verify_equal(
                "“BatteryLevel” is at 100% in the “FswStatus” message view.",
                100,
                message211.data.level,
                comment=f"Status message: {message211}",
            )

            step.verify_equal(
                "The right user LED is solid green indicating charging is OFF.",
                foot_switch.leds.LED_MODE.ON_SOLID,
                foot_switch.leds.get_led_mode(foot_switch.leds.LEDS.RIGHT_GREEN),
            )

    def test_battery_charging_led_pattern(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0213] This test verifies Battery LED pattern while battery in standby is charging.
        """
        with report.TestStep(
            "Install Battery set B in the Footswitch Cable to Console and select. "
            "(Batteries set B – more than 40% and less than 70% capacity (Battery1: 40% to 70%; Battery2: 20% ±1%).)"
        ) as step:
            foot_switch_state, message = connect_footswitch_to_console(
                foot_switch, beacons=None
            )

            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                foot_switch_state,
                comment=f"Status message: {message}",
            )

            foot_switch.batteries.battery1.set_charge_level(50)
            foot_switch.batteries.battery2.set_charge_level(20)

            self.wait_for_charging_voltage(foot_switch, charging=True)

            foot_switch.batteries.battery1.set_average_current(50)
            foot_switch.batteries.battery2.set_average_current(150)

            message210 = foot_switch.wired_conn.get_status_210()

            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                message210.foot_switch_state,
                comment=f"Status message: {message210}",
            )

            message211 = self.wait_for_battery_status(foot_switch, charging=True)
            message211.data = cast(BatteryStatus1, message211.data)

            step.verify_equal(
                "The “IsFswCharging” as true in the “FswStatus” message view.",
                True,
                message211.data.charging,
                comment=f"Status message: {message211}",
            )

            step.verify_equal(
                "The right user LED is blinking green indicating charging is ON.",
                foot_switch.leds.LED_MODE.ON_BLINKING,
                foot_switch.leds.get_led_mode(foot_switch.leds.LEDS.RIGHT_GREEN),
            )

            message211_b3 = foot_switch.wired_conn.get_status_211(
                lambda x: x.aux_type == AuxDataType.BatteryStatus3
                and x.data.average_current == 50,  # type: ignore
                timeout=1,
            )
            message211_b3.data = cast(BatteryStatus3, message211_b3.data)

            # TODO: This verification step si different from test specification where ICE debugger is is used
            # for verification. This is not the best way to verify SW functionality and we shall check the behaviour
            # using 'public' SW interface.
            step.verify_equal(
                "Average current from battery1 is in use (reported in BatteryStatus3 status message)",
                50,
                message211_b3.data.average_current,
                comment=f"Status message: {message211_b3}",
            )

            step.verify_equal(
                "Battery 2 is being charged (charging voltage is applied)",
                True,
                foot_switch.batteries.is_charging_voltage_enabled_battery2,
            )

        with report.TestStep("Press on the treadle."):
            foot_switch.treadle.down(1000)

            self.wait_for_charging_voltage(foot_switch, charging=False)

            message211 = self.wait_for_battery_status(foot_switch, charging=False)
            message211.data = cast(BatteryStatus1, message211.data)

            step.verify_equal(
                "The right user LED is solid green indicating charging is OFF.",
                foot_switch.leds.LED_MODE.ON_SOLID,
                foot_switch.leds.get_led_mode(foot_switch.leds.LEDS.RIGHT_GREEN),
            )

            step.verify_equal(
                "FswStatus” message view indicates “IsFswCharging” is OFF",
                False,
                message211.data.charging,
                comment=f"Status message: {message211}",
            )

        with report.TestStep("Release treadle.") as step:
            foot_switch.treadle.up()

            self.wait_for_charging_voltage(foot_switch, charging=True)

            step.verify_equal(
                "The right user LED is blinking green indicating charging is ON.",
                foot_switch.leds.LED_MODE.ON_BLINKING,
                foot_switch.leds.get_led_mode(foot_switch.leds.LEDS.RIGHT_GREEN),
            )

        #  TODO: Disconnect footswitch from console and cradle to left side of the console - not in scope of PoC

    def test_state_of_health(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0XXX] This test verifies that state of health of both batteries is correctly reported.
        """
        with report.TestStep("Cable Footswich to Console and select") as step:
            foot_switch_state, message = connect_footswitch_to_console(foot_switch)

            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                foot_switch_state,
                comment=f"Status message: {message}",
            )

        with report.TestStep(
            "Use battery1 with SoH 10% and battery2 with Soh 15%"
        ) as step:
            battery1_soh_set = 10
            battery2_soh_set = 15
            foot_switch.batteries.battery1.set_state_of_health(battery1_soh_set)
            foot_switch.batteries.battery2.set_state_of_health(battery2_soh_set)

            message211 = foot_switch.wired_conn.get_status_211(
                lambda x: x.aux_type == AuxDataType.BatteryDebugInfo
                and x.data.battery1_soh == battery1_soh_set  # type: ignore
                and x.data.battery2_soh == battery2_soh_set,  # type: ignore
                timeout=1,
            )
            message211.data = cast(BatteryDebugInfo, message211.data)

            step.verify_equal(
                f"FswStatus” message view indicates “Battery 1 SOH” is {battery1_soh_set}",
                battery1_soh_set,
                message211.data.battery1_soh,
                comment=f"Battery Debug Info: {message211}",
            )

            step.verify_equal(
                f"FswStatus” message view indicates “Battery 2 SOH” is {battery2_soh_set}",
                battery2_soh_set,
                message211.data.battery2_soh,
                comment=f"Battery Debug Info: {message211}",
            )
