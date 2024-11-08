from framework.apps.flacs_lgs import FlacsLgs
from framework.support.reports import report


class TestConnection:
    """! Connection Tests."""

    def test_connection(self, flacs_lgs: FlacsLgs) -> None:
        """! This test tries to connect with FlacsLgs."""
        with report.TestStep("Connect with FlacsLgs."):
            flacs_lgs.vtime.sleep(0.1)

    with report.TestStep("Disconnect FlacsLgs."):
        pass
