"""Public Interface Tests / Advisories."""

from typing import cast


from framework.communications.uvcs_footswitch.msg_types.aux_data_types import (
    AuxDataType,
    ErrorFlags,
)
from framework.communications.uvcs_footswitch.msg_types.msg_data_structures import (
    FootSwitchState,
)
from framework.apps.footswitch import FootSwitch
from framework.support.reports import report
from framework.support.reports.report_data import TestStepVerify
from tests.footswitch_tests.utils import connect_footswitch_to_console


class TestAdvisories:
    """
    Test Advisories.
    """

    @staticmethod
    def check_buttons_inactive(step: TestStepVerify, foot_switch: FootSwitch) -> None:
        """
        To check if button is inactive do following.

        Ensure that the Footswitch is horizontally oriented and top side up.
        Press down on the treadle and observe that “FswStatus” message view continues to display range 0 with 0%
        penetration.  Release treadle when done.
        Press button RV and observe that “FswStatus” message view continues to display no button activity
        (i.e. no buttons pressed).
        Repeat step 3 for buttons RH, LH, LV, R-Heel and L-Heel.
        """
        # TODO: Question: shall we position footswitch in correct position for this test?
        # Messages are not sent. Is this considered as buttons are inactive?
        foot_switch.treadle.down(200)
        message = foot_switch.wired_conn.get_status_210(
            lambda msg: msg.treadle_count != 0
        )
        if message is None:
            message = foot_switch.wired_conn.get_status_210()

        step.verify_equal(
            "Treadle is inactive",
            0,
            message.treadle_count,
            comment=f"Status message: {message}",
        )

        foot_switch.treadle.up()

        for button_name, hw_button in foot_switch.buttons.get_all_buttons():
            hw_button.press_button()
            message = foot_switch.wired_conn.get_status_210(
                lambda msg: getattr(msg.buttons, button_name) is True
            )

            step.verify_equal(
                f"{button_name} button is inactive",
                False,
                getattr(message.buttons, button_name),
                comment=f"Status message: {message.buttons}",
            )

            hw_button.release_button()

    @staticmethod
    def check_buttons_active(step: TestStepVerify, foot_switch: FootSwitch) -> None:
        """
        To check if button is active do following.

        Ensure that the Footswitch is horizontally oriented and top side up.
        Slowly and gradually press down on the treadle until it hits the bottom.
        Observe that the treadle count increases from 0 to 4095 on “FswStatus” message view.
        Release treadle slowly until it returns to the homing position.
        Observe that treadle count decreases from 4095 to 0.
        Press button RV and observe that the corresponding indicator on ’Simulator’ is on.
        Repeat step 2 for buttons RH, LH, LV, R-Heel and L-Heel.
        """
        foot_switch.treadle.down(200)
        message = foot_switch.wired_conn.get_status_210(
            lambda msg: msg.treadle_count != 0
        )

        step.verify_equal(
            "Treadle is active",
            True,
            message.treadle_count > 0,
            comment=f"Status message: {message}",
        )

        foot_switch.treadle.up()

        for button_name, hw_button in foot_switch.buttons.get_all_buttons():
            hw_button.press_button()
            message = foot_switch.wired_conn.get_status_210(
                lambda msg: getattr(msg.buttons, button_name) is True
            )

            step.verify_equal(
                f"{button_name} button is active",
                True,
                getattr(message.buttons, button_name),
                comment=f"Status message: {message.buttons}",
            )

            hw_button.release_button()

    def test_advisories_battery_comm_error(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0137] This test tests battery communication error is handled properly when cabled.
        """
        with report.TestStep(
            "Replace footswitch batteries with battery with switch, ensure battery "
            "level is > 40% and < 70%. Cable Footswitch to Console and select."
        ) as step:
            foot_switch.batteries.battery1.set_charge_level(60)
            foot_switch.batteries.battery2.set_charge_level(60)
            foot_switch_state, message = connect_footswitch_to_console(foot_switch)

            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                foot_switch_state,
                comment=f"Status message: {message}",
            )

        with report.TestStep(
            "With the treadle pressed open the battery switch."
        ) as step:
            foot_switch.treadle.down(200)

            message = foot_switch.wired_conn.get_status_210(
                lambda msg: msg.treadle_count != 0
            )
            step.verify_equal(
                "“FswStatus” message view indicates treadle is active.",
                True,
                message.treadle_count > 0,
                comment=f"Status message: {message}",
            )

            foot_switch.batteries.battery1.disconnect()
            foot_switch.batteries.battery2.disconnect()

            # TODO: After removing the battery within 2 seconds  the right user LED turns OFF
            max_wait_time = foot_switch.vtime.time_ms() + 12_000
            message211_err = None
            while foot_switch.vtime.time_ms() < max_wait_time:
                message211_err = foot_switch.wired_conn.get_status_211(
                    lambda x: x.aux_type == AuxDataType.ErrorFlags
                )
                message211_err.data = cast(ErrorFlags, message211_err.data)
                if message211_err.data.battery_comm_error:
                    break
            assert message211_err is not None
            message211_err.data = cast(ErrorFlags, message211_err.data)

            step.verify_equal(
                "After removing the battery within 2 seconds “FswStatus” indicates "
                "“IsBatteryCommError” as true",
                True,
                message211_err.data.battery_comm_error,
                f"Status message: {message211_err}",
            )

            step.verify_equal(
                "After removing the battery within 2 seconds “FswStatus” indicates "
                "“IsWirelessOpUnavailable” as true",
                True,
                message211_err.data.wireless_operation_failure,
                f"Status message: {message211_err}",
            )

        with report.TestStep("Verify that the treadle and buttons are active.") as step:
            self.check_buttons_active(step, foot_switch)

            # TODO: Verify Charging Status LED DS4 is OFF.

        with report.TestStep(
            "Release the treadle and disconnect the console-footswitch cable and press on the treadle "
            "and buttons."
        ):
            foot_switch.treadle.up()
            # TODO: disconnecting footswitch is not supported

        with report.TestStep("Cable the footswitch and press on the treadle.") as step:
            foot_switch.treadle.down(200)

            message = foot_switch.wired_conn.get_status_210()
            step.verify_equal(
                "“FswStatus” message view indicates: “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                message.foot_switch_state,
                comment=f"Status message: {message}",
            )

            message211_err = foot_switch.wired_conn.get_status_211(
                lambda x: x.aux_type == AuxDataType.ErrorFlags
            )
            message211_err.data = cast(ErrorFlags, message211_err.data)

            step.verify_equal(
                "“FswStatus” indicates “IsBatteryCommError” as true",
                True,
                message211_err.data.battery_comm_error,
                f"Status message: {message211_err}",
            )

            step.verify_equal(
                "“FswStatus” indicates “IsWirelessOpUnavailable” as true",
                True,
                message211_err.data.wireless_operation_failure,
                f"Status message: {message211_err}",
            )

            message = foot_switch.wired_conn.get_status_210(
                lambda msg: msg.treadle_count != 0
            )
            step.verify_equal(
                "“FswStatus” message view indicates: The treadle is active.",
                True,
                message.treadle_count > 0,
                comment=f"Status message: {message}",
            )

            # TODO: Charging Status LED DS4 is OFF.
            # TODO: The Battery LED (right) is OFF.
