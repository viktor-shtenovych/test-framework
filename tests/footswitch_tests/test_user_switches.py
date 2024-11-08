"""User Switches Tests."""

from framework.apps.footswitch import FootSwitch
from framework.support.reports import report
from framework.communications.uvcs_footswitch.msg_types.msg_data_structures import (
    FootSwitchState,
)
from tests.footswitch_tests.utils import connect_footswitch_to_console


class TestUserSwitches:
    """User Switches Tests."""

    def test_switches_wired(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0141] This test verifies all buttons of footswitch.
        """
        with report.TestStep("Cable Footswitch to Console and select.") as step:
            foot_switch_state, message = connect_footswitch_to_console(foot_switch)

            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                foot_switch_state,
                comment=f"Status message: {message}",
            )

        with report.TestStep(
            "Individually press, hold for at least 2 seconds, release each button listed and then verify that "
            "the correct button is active by observing “FswStatus” message view."
            "Each button is correctly indicated as active on “FswStatus” message view when pressed and cleared "
            "when released."
        ) as step:
            # TODO: increase hold timout to 2sec after emulator test timeout will be increased (currently 5 sec)
            hold_time = 0.2
            for button_name, hw_button in foot_switch.buttons.get_all_buttons():
                hw_button.press_button(hold_time)
                message = foot_switch.wired_conn.get_status_210(
                    lambda msg: getattr(msg.buttons, button_name) is True
                )
                step.verify_equal(
                    f"{button_name} button state should be True",
                    True,
                    getattr(message.buttons, button_name),
                    comment=f"Status message: {message.buttons}",
                )
                hw_button.release_button()
                message = foot_switch.wired_conn.get_status_210(
                    lambda msg: getattr(msg.buttons, button_name) is False
                )
                step.verify_equal(
                    f"{button_name} button state should be True",
                    False,
                    getattr(message.buttons, button_name),
                    comment=f"Status message: {message.buttons}",
                )

        with report.TestStep(
            "Disconnect Footswitch from Console to operate wirelessly."
        ):
            #  foot_switch.disconnect()  - TODO: not supported in emulator
            pass
