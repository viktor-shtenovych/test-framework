"""Accelerometer Tests."""

from typing import cast

from framework.communications.uvcs_footswitch.msg_types.aux_data_types import (
    AuxDataType,
    OrientationStatus,
    AccelerometerStatus,
)
from framework.core.components.position import Orientation
from framework.support.reports import report
from framework.apps.footswitch import FootSwitch
from framework.communications.uvcs_footswitch.msg_types.msg_data_structures import (
    FootSwitchState,
)
from tests.footswitch_tests.utils import (
    connect_footswitch_to_console,
    are_treadle_and_buttons_active,
)


class TestAccelerometer:
    """Accelerometer Tests."""

    def test_footswitch_orientation(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0139].

        This test verifies that the treadle and buttons are active or inactive based on the footswitch
        orientation when cabled.
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
            "With the footswitch oriented at 0° planar to the ground verify treadle and buttons are active"
        ) as step:
            orientation_status, treadle_status, button_status = (
                are_treadle_and_buttons_active(foot_switch)
            )
            step.verify_equal(
                "Verify that the Footswitch is horizontally oriented",
                True,
                orientation_status,
            )
            step.verify_equal(
                "Verify that the treadle is active",
                True,
                treadle_status,
            )
            step.verify_equal(
                "Verify that the buttons are active",
                True,
                button_status,
            )

        for button_name, button in foot_switch.buttons.get_all_buttons():
            with report.TestStep(f"Press and hold button {button_name}") as step:
                button.press_button()
                message = foot_switch.wired_conn.get_status_210(
                    lambda msg: getattr(msg.buttons, button_name) is True
                )
                step.verify_equal(
                    f"The button {button_name} indicator on “FswStatus” message view "
                    f"“IsSurgicalRightHorzBtnPressed” as true",
                    True,
                    getattr(message.buttons, button_name),
                    comment=f"Status message: {message.buttons}",
                )

                message211 = foot_switch.wired_conn.get_status_211(
                    lambda x: x.aux_type == AuxDataType.AccelerometerStatus
                    and x.data.footswitch_orientation == OrientationStatus.FacingUp  # type: ignore
                )
                message211.data = cast(AccelerometerStatus, message211.data)
                step.verify_equal(
                    "The Footswitch orientation in “Accelerator status” is “FacingUp”.",
                    OrientationStatus.FacingUp,
                    message211.data.footswitch_orientation,
                    comment=f"Status message: {message211}",
                )

            with report.TestStep(
                "Start tilting the Footswitch while monitoring the tilt angle such that the orientation angle "
                "starts slowly increasing"
            ) as step:
                # As accelerometer chip reports only few positions and not specific angles
                # we immediately switch to wrong position
                foot_switch.position.set_position(Orientation.vertical_up)

                message = foot_switch.wired_conn.get_status_210(
                    lambda msg: getattr(msg.buttons, button_name) is False
                )
                step.verify_equal(
                    "The button indicator changes from true to false when the Footswitch is tilted "
                    "by 42.5° ± 10°",
                    False,
                    getattr(message.buttons, button_name),
                    comment=f"Status message: {message.buttons}",
                )

                message211 = foot_switch.wired_conn.get_status_211(
                    lambda x: x.aux_type == AuxDataType.AccelerometerStatus
                    and x.data.footswitch_orientation == OrientationStatus.VerticalUp,  # type: ignore
                )
                message211.data = cast(AccelerometerStatus, message211.data)
                step.verify_equal(
                    "the Footswitch orientation in “Accelerator status” is VerticalUp.",
                    OrientationStatus.VerticalUp,
                    message211.data.footswitch_orientation,
                    comment=f"Status message: {message211}",
                )

            foot_switch.position.set_position(Orientation.face_up)
            button.release_button()

        with report.TestStep(
            "With the Footswich oriented at 0° planar to the ground press the treadle until it hits the bottom and "
            "hold it down"
        ) as step:
            treadle_counter = 4095
            foot_switch.treadle.down(treadle_counter)

            message210 = foot_switch.wired_conn.get_status_210(
                lambda x: x.treadle_count == treadle_counter
            )
            step.verify_equal(
                "“FswStatus” message view displays treadle count as 4095.",
                treadle_counter,
                message210.treadle_count,
                comment=f"Status message: {message210}",
            )

        with report.TestStep(
            "Start tilling the Footswitch while monitoring the tilt angle such that the orientation angle starts "
            "increasing slowly"
        ):
            foot_switch.position.set_position(Orientation.vertical_up)

            message210 = foot_switch.wired_conn.get_status_210(
                lambda x: x.treadle_count == 0
            )
            step.verify_equal(
                "The treadle count becomes zero when the Footswitch is tilted by 42.5° ± 10°, "
                "beyond which the treadle count remains at zero.",
                0,
                message210.treadle_count,
                comment=f"Status message: {message210}",
            )
