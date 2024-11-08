from typing import Tuple, Iterator
import re
import _pytest.config
import pytest

from framework.support.reports.report import TestReport


TCP_PORT_ARG_NAME = "--rpc-port"


def pytest_addoption(parser: _pytest.config.argparsing.Parser) -> None:
    """Pytest commandline adaptation."""
    parser.addoption(
        "--emulator",
        action="store",
        default=None,
        help="Command to start emulator",
    )

    parser.addoption(
        TCP_PORT_ARG_NAME,
        action="store",
        default=50051,
        help="TCP port used for RPC communication between test framework and emulator",
    )

    parser.addoption(
        "--report-docx",
        action="store",
        default=None,
        help="Generate docx test report",
    )


# Pytest hooks for reporting


def get_test_docstring(item: pytest.Function) -> Tuple[str, str, str]:
    """Method returns current test(item) docstring."""
    # check if test parametrized, get test name
    test_name = item.originalname if item.originalname else item.name

    # check if Test has Test Class, get test function
    test_func = (
        getattr(item.cls, test_name) if item.cls else getattr(item.module, test_name)
    )

    group = item.module.__doc__ if item.module.__doc__ else "OrphanGroup"
    description = str(test_func.__doc__).strip()
    match = re.match(r"(\[FSW.*])(.*)", description)
    if match:
        test_id, description = match.groups()
        return test_id, description, group
    return "", description, group


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item: pytest.Function) -> Iterator[None]:
    """Pytest hook for test setup phase.

    During setup phase the environment is fetched from the pytest commandline
    option and based on this, the node configuration is loaded.

    More info about the pytest hook:
    https://docs.pytest.org/en/stable/reference.html?#pytest.hookspec.pytest_runtest_setup
    """
    TestReport.start_test_case(*get_test_docstring(item))

    yield


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """Pytest hook to access status of test case phases."""
    if report.skipped:
        TestReport.skip_test_case()
    if report.when == "teardown":
        TestReport.finish_test_case(report.passed)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Called after whole test run finished, right before returning the exit status to the system."""
    if not session.config.getoption("--collect-only"):
        report_path = session.config.getoption("--report-docx")
        if report_path:
            TestReport.generate_report(report_path)
