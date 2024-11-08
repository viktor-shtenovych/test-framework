from enum import Enum

from framework.core.devices.accelerometer_device_ADXL346 import (
    AccelerometerDeviceADXL346,
    RawOrientation,
)


class Orientation(Enum):
    """
    Orientation.
    """

    face_up = RawOrientation.kZ_Negative
    face_down = RawOrientation.kZ_Positive
    left = RawOrientation.kY_Negative
    right = RawOrientation.kY_Positive
    vertical_up = RawOrientation.kX_Negative
    vertical_down = RawOrientation.kX_Positive
    tilted = RawOrientation.kTilted


DEFAULT_2D_VALUE = 0x00
VALID_2D = 0x40
VALID_3D = 0x08


class Position:
    """
    Position.
    """

    def __init__(self, accelerometer: AccelerometerDeviceADXL346):
        self.accelerometer = accelerometer

    def set_position(self, orientation: Orientation) -> None:
        """
        Set position.

        Args:
            orientation: Orientation.
        """
        self.accelerometer.set_orientation(
            VALID_2D | DEFAULT_2D_VALUE | VALID_3D | orientation.value
        )
