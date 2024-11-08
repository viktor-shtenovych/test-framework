from framework.support.reports import logger, report_docx
from framework.support.reports.report_data import TestStepVerify, TestCase


class TestReport:
    """Test report context manager."""

    test_cases: list[TestCase] = []

    @staticmethod
    def start_test_case(test_id: str, summary: str, group: str) -> None:
        """
        Start test case.
        """
        TestReport.test_cases.append(TestCase(test_id, summary, group))

    @staticmethod
    def current_test_case() -> TestCase | None:
        """
        Get current test case.
        """
        if TestReport.test_cases:
            return TestReport.test_cases[-1]
        return None

    @staticmethod
    def skip_test_case() -> None:
        """
        Skip test case.
        """
        testcase = TestReport.current_test_case()
        if testcase:
            testcase.skip()

    @staticmethod
    def finish_test_case(passed: bool) -> None:
        """
        Finish test case.
        """
        testcase = TestReport.current_test_case()
        if testcase:
            testcase.add_result(passed)

    @staticmethod
    def generate_report(path: str) -> None:
        """
        Generate report.
        """
        report_docx.generate_report(TestReport.test_cases, path)


class TestStep:
    """Test step context manager.

    Example:
        >>> with TestStep("Perform action XY") as step:
        >>>     a = 1
        >>>     b = 1
        >>>     step.verify_equal("Check that a equals to b", a, b)
    """

    def __init__(self, action: str, expected: str | None = None):
        self._action = action
        self._expected = expected

    def __enter__(self) -> TestStepVerify:
        """
        Enter the context.
        """
        logger.test_action(f"{self._action}")  # type: ignore
        step = TestStepVerify(self._action)
        test_case = TestReport.current_test_case()
        if test_case:
            test_case.add_test_step(step)
        return step

    def __exit__(self, type, value, traceback) -> bool:  # type: ignore
        """
        Exit the context.
        """
        if type:
            return False
        return True
