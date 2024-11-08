"""Safety Tests."""

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
from tests.footswitch_tests.utils import connect_footswitch_to_console


class TestSafety:
    """
    Test Safety.
    """

    def test_safety_irrespective_encoder(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0153A].

        This test verifies that reported treadle count is zero when the treadle is up irrespective
        of the measured encoder position.
        """
        with report.TestStep(
            "Connect the standalone encoder with gearbox to connector J9 and J4.  To avoid an encoder failure, "
            "disconnect the battery before connecting the encoder and reconnect the battery afterwards."
        ) as step:
            foot_switch_state, message = connect_footswitch_to_console(foot_switch)

            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                foot_switch_state,
                comment=f"Status message: {message}",
            )

        with report.TestStep("Cable Footswitch to the Console and select.") as step:
            # Already connected in previous step

            message = foot_switch.wired_conn.get_status_210()

            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                message.foot_switch_state,
                comment=f"Status message: {message}",
            )

        with report.TestStep("Press and hold down the treadle.") as step:
            # Simulate pressing treadle by releasing all 'up switches' but still indicating 0 in encoder
            encoder_value = foot_switch.treadle.encoder.get_value()
            foot_switch.treadle.down(treadle_counter=0, strength=5)
            foot_switch.treadle.encoder.set_value(encoder_value)

            message = foot_switch.wired_conn.get_status_210()

            step.verify_equal(
                "“FswStatus” message view displays zero treadle count.",
                0,
                message.treadle_count,
                comment=f"Status message: {message}",
            )

        with report.TestStep(
            "Rotate the gear counterclockwise such that the treadle count is 2000 ± 200."
        ) as step:
            encoder_step = 10
            encoder_value = encoder_value
            treadle_counter = 0
            max_wait_time = foot_switch.vtime.time_ms() + 1_000

            while (
                treadle_counter < 1800 and foot_switch.vtime.time_ms() < max_wait_time
            ):
                encoder_value += encoder_step
                foot_switch.treadle.encoder.set_value(encoder_value)

                message = foot_switch.wired_conn.get_status_210(
                    lambda msg: msg.treadle_count != treadle_counter
                )
                treadle_counter = message.treadle_count

            message = foot_switch.wired_conn.get_status_210()

            step.verify_equal(
                "Treadle count changes in response to the gear rotation.  “FswStatus” message view displays "
                "treadle count at roughly 2000 ± 200. ",
                True,
                1800 < message.treadle_count < 2200,
                comment=f"Status message: {message}. Treadle counter = {message.treadle_count}",
            )

        with report.TestStep("Release the treadle.") as step:
            # Simulate releasing treadle by releasing all 'up switches' (strength = 0) but still indicating
            # current value in encoder
            foot_switch.treadle.up()
            foot_switch.treadle.encoder.set_value(encoder_value)

            message = foot_switch.wired_conn.get_status_210(
                lambda msg: msg.treadle_count == 0
            )
            step.verify_equal(
                "FswStatus” shows treadle count as 0 as soon as the treadle is up. ",
                0,
                message.treadle_count,
                comment=f"Status message: {message}. Treadle counter = {message.treadle_count}",
            )

            max_wait_time = foot_switch.vtime.time_ms() + 1_000
            while foot_switch.vtime.time_ms() < max_wait_time:
                message211_err = foot_switch.wired_conn.get_status_211(
                    lambda x: x.aux_type == AuxDataType.ErrorFlags
                )
                message211_err.data = cast(ErrorFlags, message211_err.data)

                if message211_err.data.up_switch_failure is True:
                    break

            message211_err.data = cast(ErrorFlags, message211_err.data)

            step.verify_equal(
                "“FswStatus” indicates “IsUpSwitchFailure” as true.",
                True,
                message211_err.data.up_switch_failure,
                comment=f"Status message: {message211_err}."
                f" Up switch failure = {message211_err.data.up_switch_failure}",
            )

            # TODO: Un-cable and cable footswitch to console, after 2 seconds un-cable footswitch for wireless
            #  operation. Repeat Steps 3 thru 5.
