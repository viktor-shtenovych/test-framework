import struct
from typing import Iterator

import pytest

from framework.core.devices.battery_pack_manager_bq40z50 import (
    BatteryPackManagerBq40z50,
)


@pytest.fixture
def battery_pack() -> Iterator[BatteryPackManagerBq40z50]:
    """
    Fixture for BatteryPackManagerBq40z50.
    """
    yield BatteryPackManagerBq40z50(instance_id=0, address=1)


def test_charge_level(battery_pack: BatteryPackManagerBq40z50) -> None:
    """
    Test charge level.
    """
    level = 80
    battery_pack.set_charge_level(level)

    battery_pack.write(bytes([0x0D]))  # address of RelativeStateOfCharge
    assert battery_pack.read(2) == struct.pack("<H", level)
