import dataclasses
from enum import IntEnum

import bitstruct


class FootSwitchType(IntEnum):
    """
    Foot switch types.
    """

    Centurion = 0
    Microscope = 1
    UvcsCombined = 2
    UvcsAnterior = 3


class FootSwitchState(IntEnum):
    """
    Foot switch states.
    """

    Cabled = 0
    Cradled = 1
    Active = 2
    Sleep = 3


@dataclasses.dataclass
class Buttons:
    """
    Foot switch buttons.
    """

    calibrated: bool
    right_horizontal: bool
    right_vertical: bool
    left_horizontal: bool
    left_vertical: bool
    recovered_from_timeout: bool
    right_heel: bool
    left_heel: bool

    @classmethod
    def unpack(cls, data: bytes) -> "Buttons":
        """
        Unpacks the data into a Buttons object.
        """
        return Buttons(*tuple(reversed(bitstruct.unpack("<b1b1b1b1b1b1b1b1", data))))


@dataclasses.dataclass
class LaserButtons:
    """
    Laser foot switch buttons.
    """

    connected: bool
    right: bool
    center: bool
    left: bool
    shroud_up_detected: bool

    @classmethod
    def unpack(cls, data: bytes) -> "LaserButtons":
        """
        Unpacks the data into a LaserButtons object.
        """
        return LaserButtons(*tuple(reversed(bitstruct.unpack("p3b1b1b1b1b1", data))))
