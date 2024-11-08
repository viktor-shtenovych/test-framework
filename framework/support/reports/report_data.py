from typing import Any, List, Tuple

from pytest_check import check

from framework.support.reports import logger


class TestStepVerify:
    """Support for test step verification. There can be multiple verifications for one test step action."""

    def __init__(self, action: str) -> None:
        self.action = action
        self.verifications: List[Tuple[bool, str]] = []

    def verify_equal(
        self, verify_msg: str, expected: Any, actual: Any, comment: str | None = None
    ) -> None:
        """
        Verify that the expected and actual values are equal.

        Args:
            verify_msg (str): The message to display in the report.
            expected (Any): The expected value.
            actual (Any): The actual value.
            comment (str, optional): A comment to display in the report. Defaults to None.
        """
        passed = check.equal(expected, actual, comment)
        # Marks: \u2713  \u2714 \u2717 \u2718
        mark = "\u2713" if passed else "\u2717"
        logger.verify(f"{mark} {verify_msg}")  # type: ignore
        if comment:
            logger.info(comment)
        else:
            logger.info(f"Expected: {expected}, actual: {actual}")
        self.verifications.append((passed, verify_msg))


class TestCase:
    """
    A class to represent a test case.

    Attributes:
        test_id (str): The ID of the test case.
        summary (str): The summary of the test case.
        group (str): The group the test case belongs to.
        steps (List[TestStepVerify]): The steps of the test case.
        result (bool | None): The result of the test case.
        skipped (bool): A flag to indicate whether the test case was skipped.
    """

    def __init__(self, test_id: str, summary: str, group: str) -> None:
        self.test_id = test_id
        self.summary = summary
        self.group = group
        self.steps: List[TestStepVerify] = []
        self.result: bool | None = None
        self.skipped = False

    def add_test_step(self, step: TestStepVerify) -> None:
        """
        Add a test step to the test case.

        Args:
            step (TestStepVerify): The test step to add.
        """
        self.steps.append(step)

    def add_result(self, result: bool) -> None:
        """
        Add the result of the test case.

        Args:
            result (bool): The result of the test case.
        """
        self.result = result

    def skip(self) -> None:
        """
        Skip the test case.
        """
        self.skipped = True
