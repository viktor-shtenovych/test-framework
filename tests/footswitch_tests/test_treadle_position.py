"""Treadle position Tests."""

import pytest

from framework.communications.uvcs_footswitch.msg_types.real_time_status_msgs import (
    StatusMsg210,
)
from framework.communications.uvcs_footswitch.msg_types.msg_data_structures import (
    FootSwitchState,
)
from framework.communications.uvcs_console.wired.wiredconn import CanMsgTimeoutError
from framework.apps.footswitch import FootSwitch
from framework.support.reports import report, logger
from tests.footswitch_tests.utils import connect_footswitch_to_console


class TestTreadlePosition:
    """Treadle position Tests."""

    def perform_treadle_action(
        self,
        count: int,
        foot_switch: FootSwitch,
        previous_value: int,
        treadle_increment_step: int = 100,
    ) -> StatusMsg210:
        """
        Perform treadle action.
        """
        foot_switch.treadle.down(count * treadle_increment_step)
        try:
            message = self.get_next_treadle_status(foot_switch, previous_value)
        except CanMsgTimeoutError:
            raise AssertionError("Timeout waiting for treadle count to change")
        return message

    def get_next_treadle_status(
        self, foot_switch: FootSwitch, previous_value: int
    ) -> StatusMsg210:
        """
        Get next treadle status.
        """
        return foot_switch.wired_conn.get_status_210(
            lambda msg: msg.treadle_count != previous_value, timeout=0.5
        )

    def test_treadle_linear_increment(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0142] Verify that treadle count linearly increments and decrements with treadle movement.
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
            "Verify treadle count increments and decrements linearly."
        ) as step:
            message = foot_switch.wired_conn.get_status_210()
            assert message is not None
            previous_value = message.treadle_count
            start_treadle_counter = 100
            max_treadle_counter = 4095
            foot_switch.treadle.down(start_treadle_counter)
            message = self.get_next_treadle_status(foot_switch, previous_value)
            assert message is not None
            previous_value = message.treadle_count
            is_treadle_count_increasing = True
            for count in range(2, 41):
                message = self.perform_treadle_action(
                    count, foot_switch, previous_value
                )
                previous_value = message.treadle_count
                treadle_count = message.treadle_count
                logger.debug(f"Treadle count: {treadle_count}")
                if treadle_count != pytest.approx(count * 100, abs=5):
                    is_treadle_count_increasing = False
                    break
            step.verify_equal(
                "Treadle count should increase linearly",
                True,
                is_treadle_count_increasing,
            )
        with report.TestStep(
            "Verify treadle count should increase to maximum value 4095"
        ) as step:
            message = self.perform_treadle_action(
                max_treadle_counter,
                foot_switch,
                previous_value,
                treadle_increment_step=1,
            )

            step.verify_equal(
                "Treadle count should increase to 4095",
                max_treadle_counter,
                message.treadle_count,
            )
            previous_value = message.treadle_count

        with report.TestStep(
            "Release the treadle until it returns to its up position."
        ) as step:
            foot_switch.treadle.up()
            message = foot_switch.wired_conn.get_status_210(
                lambda msg: msg.treadle_count != previous_value
            )
            step.verify_equal(
                "Treadle count should decrease",
                0,
                message.treadle_count,
            )
            previous_value = message.treadle_count
