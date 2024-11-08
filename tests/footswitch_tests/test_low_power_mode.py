"""Low-Power Mode Tests."""

from framework.communications.uvcs_footswitch.msg_types.msg_data_structures import (
    FootSwitchState,
)
from framework.apps.footswitch import FootSwitch
from framework.support.reports import report
from tests.footswitch_tests.utils import connect_footswitch_to_console


class TestLowPowerMode:
    """Low-Power Mode Tests."""

    def test_low_power_wakeup_upswitch(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0202B].

         This test verifies that a change of state on any of the up-switch signals wakes up the CPU
         from the low power mode. Use UVCS Anterior Footswitch

        """
        with report.TestStep(
            "With the footswitch facing up cable Footswitch to Console and select. "
            "Trigger the up-switch."
        ) as step:
            foot_switch_state, message = connect_footswitch_to_console(foot_switch)

            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                foot_switch_state,
                comment=f"Status message: {message}",
            )

        with report.TestStep(
            "For each of the 5 up-switches do the following: (Note observed timed in table below)"
        ) as step:
            for switch in foot_switch.treadle._switches:
                # Release the up-switch under test and keep at least 3 other up switches triggered.
                switch.release_button()

                # TODO: The signal on CH1 transitions to logic 0 indicating the CPU is in low power mode.

                # TODO: Upon pressing the up-switch the signal on CH1 transitions to logic 1 indicating CPU exiting
                #  low power mode. Within 0.9± 0.2 seconds CH1 transitions to logic 0 indicating CPU re-entering
                #  low power mode.

                # TODO: Upon releasing the up-switch the signal on CH1 transitions to logic 1 indicating CPU exiting
                #  low power mode. Within 0.9± 0.2 seconds CH1 transitions to logic 0 indicating CPU re-entering
                #  low power mode.

                switch.press_button()
