import pytest

from framework.support.reports import log
from framework.support.vtime import vtime_manager


@pytest.fixture(scope="session", autouse=True)
def fixture_virtual_time() -> None:
    """
    Fixture for virtual time.
    """
    log.register_virtual_time_func(vtime_manager.time_ms)
