from typing import cast, Tuple, Optional

from framework.apps.footswitch import FootSwitch
from framework.communications.uvcs_footswitch.msg_types.real_time_status_msgs import (
    StatusMsg210,
    StatusMsg211,
)
from framework.communications.uvcs_footswitch.msg_types.configuration_msg import (
    ConfigurationMsg310,
    ConfigurationMsg311,
)
from framework.communications.uvcs_footswitch.msg_types.aux_data_types import (
    AuxDataType,
    AccelerometerStatus,
    OrientationStatus,
)
from framework.communications.uvcs_footswitch.msg_types.msg_data_structures import (
    FootSwitchState,
    Buttons,
)
from framework.support.reports import logger


def connect_footswitch_to_console(
    foot_switch: FootSwitch,
    period: float = 0.08,
    beacons: Optional[list[ConfigurationMsg310 | ConfigurationMsg311]] = [
        ConfigurationMsg310(),
        ConfigurationMsg311(),
    ],
) -> Tuple[FootSwitchState, StatusMsg210]:
    """
    Connects the footswitch to the console and enables beacons.

    This function connects the footswitch, sets the treadle to the up position, enables beacons, and retrieves the status.

    Args:
        foot_switch (FootSwitch): The footswitch to connect.
        period (float, optional): The period for the beacons. Defaults to 0.08.
        beacons (Optional[list[ConfigurationMsg310 | ConfigurationMsg311]], optional): The beacons to enable. Defaults to [ConfigurationMsg310(), ConfigurationMsg311()].

    Returns:
        Tuple[FootSwitchState, StatusMsg210]: The state of the footswitch and the status message.

    Note:
        The LED at DS1 is blinking at approximately 1 Hz.
    """
    foot_switch.connect()
    foot_switch.treadle.up()
    foot_switch.wired_conn.enable_beacons(period=period, beacons=beacons)
    message = foot_switch.wired_conn.get_status_210()
    # TODO The LED at DS1 is blinking at approximately 1 Hz
    return message.foot_switch_state, message


def _verify_button_state(
    foot_switch: FootSwitch, button_name: str, expected_state: bool
) -> Tuple[Buttons, bool]:
    """
    Return the state of a button in the 'FswStatus' message view.
    """
    message = foot_switch.wired_conn.get_status_210(
        lambda msg: getattr(msg.buttons, button_name) is expected_state
    )
    result = getattr(message.buttons, button_name)

    return message.buttons, result


def are_treadle_and_buttons_active(
    foot_switch: FootSwitch,
) -> Tuple[bool, bool, bool]:
    """
    To verify that the treadle and buttons are active do the following.

    1.  Ensure that the Footswitch is horizontally oriented and top side up.
    2.  Slowly and gradually press down on the treadle until it hits the bottom.
        Observe that the treadle count increases from 0 to 4095 on “FswStatus” message view.
        Release treadle slowly until it returns to the homing position.
        Observe that treadle count decreases from 4095 to 0.
    3.  Press button RV and observe that the corresponding indicator on 'Simulator' is on.
    4.  Repeat step 2 for buttons RH, LH, LV, R-Heel and L-Heel.

    """
    orientation_status = False
    treadle_status = False
    buttons_status = False
    logger.info("Ensure that the Footswitch is horizontally oriented and top side up")
    orientation, message = _get_orientation_facing_up(foot_switch)
    if orientation is OrientationStatus.FacingUp:
        orientation_status = True

    logger.info(
        "Slowly and gradually press down on the treadle until it hits the bottom. "
        "Observe that the treadle count increases from 0 to 4095 on “FswStatus” message view. "
    )
    treadle_position = _get_treadle_position(foot_switch)
    if treadle_position == 0:
        _press_down_treadle_slowly(foot_switch)
        logger.info(
            "Release treadle slowly until it returns to the homing position."
            "Observe that treadle count decreases from 4095 to 0."
        )
        treadle_position = _get_treadle_position(foot_switch)
        if treadle_position == 4095:
            release_treadle_slowly(foot_switch)
            treadle_position = _get_treadle_position(foot_switch)
            if treadle_position == 0:
                treadle_status = True

    logger.info(
        "Press button RV and observe that the corresponding indicator on 'Simulator' is on."
        "Repeat this step for buttons RH, LH, LV, R-Heel and L-Heel."
    )
    buttons_status = verify_buttons_active(foot_switch)

    return orientation_status, treadle_status, buttons_status


def _get_orientation_facing_up(
    foot_switch: FootSwitch,
) -> Tuple[OrientationStatus, StatusMsg211]:
    """
    Return the orientation status of the footswitch.

    The footswitch should be horizontally oriented and top side up.

    Args:
        foot_switch (FootSwitch): The footswitch to connect.

    Returns:
        Tuple[OrientationStatus, StatusMsg211]: The orientation status of the footswitch and the status message.
    """
    message_211 = foot_switch.wired_conn.get_status_211(
        lambda x: x.aux_type == AuxDataType.AccelerometerStatus
        and x.data.footswitch_orientation == OrientationStatus.FacingUp  # type: ignore
    )
    message_211.data = cast(AccelerometerStatus, message_211.data)

    return message_211.data.footswitch_orientation, message_211


def _get_treadle_position(foot_switch: FootSwitch) -> int:
    """
    Retrieves the current position of the treadle on the footswitch.

    This function gets the status of the footswitch and returns the treadle count,
    which represents the current position of the treadle.

    Args:
        foot_switch (FootSwitch): The footswitch to get the treadle position from.

    Returns:
        int: The current position of the treadle.
    """
    message_210 = foot_switch.wired_conn.get_status_210()
    treadle_position = message_210.treadle_count
    return treadle_position


def _press_down_treadle_slowly(foot_switch: FootSwitch) -> None:
    """
    Simulates a slow press down on the footswitch's treadle.

    This function gradually increases the treadle count from 0 to 5000 in steps of 1000,
    simulating a slow press down on the treadle. After each step, it retrieves the status
    of the footswitch and updates the treadle position.

    Args:
        foot_switch (FootSwitch): The footswitch to press down on.

    Note:
        This is a private function and should not be called directly.
    """
    treadle_position = 0
    for position in range(1, 6):
        foot_switch.treadle.down(position * 1000)
        message_210 = foot_switch.wired_conn.get_status_210(
            lambda msg: msg.treadle_count > treadle_position
        )
        treadle_position = message_210.treadle_count


def release_treadle_slowly(foot_switch: FootSwitch) -> None:
    """
    Simulates a slow release of the footswitch's treadle.

    This function gradually decreases the treadle count from 4095 to 0 in steps of 1000,
    simulating a slow release of the treadle. After each step, it retrieves the status
    of the footswitch and updates the treadle position.

    Args:
        foot_switch (FootSwitch): The footswitch to release.
    """
    treadle_position = 4095
    for position in range(3, -1, -1):
        foot_switch.treadle.down(position * 1000)
        message_210 = foot_switch.wired_conn.get_status_210(
            lambda msg: msg.treadle_count != treadle_position
        )
        treadle_position = message_210.treadle_count


def verify_buttons_active(foot_switch: FootSwitch) -> bool:
    """
    Verifies if all buttons on the footswitch are active.

    This function iterates over all buttons on the footswitch, pressing and releasing each one.
    It verifies the state of each button after pressing and releasing, and returns False if any button is not in the expected state.

    Args:
        foot_switch (FootSwitch): The footswitch to verify.

    Returns:
        bool: True if all buttons are active, False otherwise.
    """
    button_status = True
    for button_name, hw_button in foot_switch.buttons.get_all_buttons():
        hw_button.press_button()
        message, result = _verify_button_state(foot_switch, button_name, True)
        if not result:
            logger.debug(f"{button_name} button is not pressed")
            logger.debug(f"Status message {message}")
            button_status = False
            return button_status

        hw_button.release_button()
        message, result = _verify_button_state(foot_switch, button_name, False)
        if result:
            logger.debug(f"{button_name} button is not released")
            logger.debug(f"Status message {message}")
            button_status = False
            return button_status
    return button_status
