import struct
from typing import Iterator

import pytest

from framework.core.devices.accelerometer_device_ADXL346 import (
    AccelerometerDeviceADXL346,
)


@pytest.fixture
def Accelerometer() -> Iterator[AccelerometerDeviceADXL346]:
    """
    Create an Accelerometer.

    Returns:
        Accelerometer: An Accelerometer.
    """
    yield AccelerometerDeviceADXL346(instance_id=0, address=1)


def test_orientation(Accelerometer: AccelerometerDeviceADXL346) -> None:
    """
    Test orientation.

    Args:
        Accelerometer: An Accelerometer.
    """
    orientation = 11
    Accelerometer.set_orientation(orientation)

    Accelerometer.write(bytes([0x00, 0xBC]))  # address of Orientation status
    assert Accelerometer.read(2) == struct.pack("<H", orientation)
