"""Detent/vibration Tests."""

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
from framework.communications.uvcs_footswitch.msg_types.configuration_msg import (
    ConfigurationMsg311,
    ConfigurationMsg310,
)

DETENT_POSITIONS = [620, 2200]


def get_treadle_count_from_message(foot_switch: FootSwitch, start_value: int) -> int:
    """
    Get the treadle count from the message.

    Args:
        foot_switch (FootSwitch): The foot switch.
        start_value (int): The start value.

    Returns:
        int: The treadle count.
    """
    message = foot_switch.wired_conn.get_status_210(
        lambda msg: msg.treadle_count != start_value
    )
    return message.treadle_count


class TestTreadleDetentVibration:
    """
    Test Treadle Detent Vibration.

    This test verifies detent vibrations in the Unity Anterior Footswitch.
    """

    def perform_treadle_action(
        self, count: int, foot_switch: FootSwitch, previous_value: int
    ) -> StatusMsg210 | None:
        """
        Perform the treadle action.

        Args:
            count (int): The count.
            foot_switch (FootSwitch): The foot switch.
            previous_value (int): The previous value.

        Returns:
            StatusMsg210 | None: The message.
        """
        foot_switch.treadle.clear_detent_detection()
        foot_switch.treadle.down(count * 10)
        try:
            message = foot_switch.wired_conn.get_status_210(
                lambda msg: msg.treadle_count != previous_value, timeout=0.5
            )
        except CanMsgTimeoutError:
            return None
        return message

    def test_treadle_detent_vibration(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0145] This test verifies detent vibrations in the Unity Anterior Footswitch.
        """
        with report.TestStep("Cable Footswitch to Console and select.") as step:
            """
            example of calculating detent positions configuration in emulator:
            position1_counts = ( kTreadleDetentMaxCounts * detent_position1_counts ) /
                                kTreadleDetentMaxPercent;
            int32_t region0_start = config_.position1_counts -
            ( kDetentStartOffsetCounts + region1_hysteresis_counts_ );
            """
            foot_switch_state, message = connect_footswitch_to_console(
                foot_switch,
                period=0.2,
                beacons=[
                    ConfigurationMsg310(),
                    ConfigurationMsg311(detent_position_1=18, detent_position_2=56),
                ],
            )
            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                foot_switch_state,
                comment=f"Status message: {message}",
            )

        with report.TestStep(
            "Starting from treadle up position, slowly press the treadle all the way down and slowly release"
            " all the way up to the treadle up position by hand while observing the “SurgicalRawTreadleCount”"
            " field in the “FswStatus” message view."
        ) as step:
            message = foot_switch.wired_conn.get_status_210()
            previous_value = message.treadle_count
            start_treadle_counter = 100
            max_treadle_counter = 250
            foot_switch.treadle.down(start_treadle_counter)
            message = foot_switch.wired_conn.get_status_210(
                lambda msg: msg.treadle_count != previous_value
            )

            previous_value = message.treadle_count
            logger.info(f"Initial treadle count: {previous_value}")

            first_detent_occurred = False
            second_detent_occurred = False
            other_detent_occurred = False

            # Press the treadle down slowly and check for vibrations
            for count in range(2, max_treadle_counter):
                message_treadle = self.perform_treadle_action(
                    count, foot_switch, previous_value
                )
                assert message_treadle is not None
                previous_value = message_treadle.treadle_count
                treadle_count = message_treadle.treadle_count
                logger.debug(f"Treadle count: {treadle_count}")
                foot_switch.vtime.sleep(0.15)
                if treadle_count == pytest.approx(DETENT_POSITIONS[0], abs=20):
                    if foot_switch.treadle.is_detent_occurred():
                        first_detent_occurred = True
                elif treadle_count == pytest.approx(DETENT_POSITIONS[1], abs=20):
                    if foot_switch.treadle.is_detent_occurred():
                        second_detent_occurred = True
                elif foot_switch.treadle.is_detent_occurred():
                    other_detent_occurred = True

            step.verify_equal(
                "First detent vibration should be triggered at 620±10 counts",
                True,
                first_detent_occurred,
            )
            step.verify_equal(
                "Second detent vibration should be triggered at 2200±10 counts",
                True,
                second_detent_occurred,
            )
            step.verify_equal(
                "No other vibrations should be felt",
                False,
                other_detent_occurred,
            )

            other_detent_occurred = False

            # Release the treadle slowly and check for vibrations
            for count in range(max_treadle_counter - 1, 1, -1):
                message_treadle = self.perform_treadle_action(
                    count, foot_switch, previous_value
                )
                foot_switch.vtime.sleep(0.15)
                if message_treadle is not None:
                    previous_value = message_treadle.treadle_count
                    treadle_count = message_treadle.treadle_count
                    logger.debug(f"Treadle count: {treadle_count}")
                    if foot_switch.treadle.is_detent_occurred():
                        other_detent_occurred = True
            step.verify_equal(
                "No other vibrations should be felt",
                False,
                other_detent_occurred,
            )
