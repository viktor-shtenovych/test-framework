import functools
import logging
import sys
import time
import traceback
from typing import Any, Callable, TypeVar, cast


def add_logging_level(
    level_name: str, level_num: int, method_name: str | None = None
) -> None:
    """Comprehensively adds a new logging level to the `logging` module and the currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example:
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5
    """
    if not method_name:
        method_name = level_name.lower()

    if hasattr(logging, level_name):
        raise AttributeError("{} already defined in logging module".format(level_name))
    if hasattr(logging, method_name):
        raise AttributeError("{} already defined in logging module".format(method_name))
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError("{} already defined in logger class".format(method_name))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def log_for_level(self: Any, message: str, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(level_num):
            self._log(level_num, message, args, **kwargs)

    def log_to_root(message: str, *args: Any, **kwargs: Any) -> None:
        logging.log(level_num, message, *args, **kwargs)

    logging.addLevelName(level_num, level_name)
    setattr(logging, level_name, level_num)
    setattr(logging.getLoggerClass(), method_name, log_for_level)
    setattr(logging, method_name, log_to_root)


class AddVirtualTimeFilter(logging.Filter):
    """
    This class is a custom logging filter that adds a virtual time attribute to log records.

    Attributes:
        get_time_func: A callable that returns the current virtual time. The return type can be int or str.
    """

    def __init__(self) -> None:
        self.get_time_func: Callable[[], int | str] | None = None

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Adds a virtual time attribute to the log record.

        Args:
            record: The log record to which the virtual time attribute is added.

        Returns:
            Always returns True so that the log record is not filtered out.
        """
        record.vtime = self.get_time_func() if self.get_time_func is not None else "-"
        return True


__vtime_filter = AddVirtualTimeFilter()

add_logging_level("ACTION", logging.WARNING + 5, "test_action")
add_logging_level("VERIFY", logging.WARNING + 3)
logger = logging.getLogger(__name__)
logger.addFilter(__vtime_filter)


def register_virtual_time_func(func: Callable[[], int]) -> None:
    """Registers a function that returns the current virtual time.

    This function is used by the AddVirtualTimeFilter to add a virtual time attribute to log records.

    Args:
        func: A callable that returns the current virtual time as an integer.
    """
    __vtime_filter.get_time_func = func


def configure_logger_for_script() -> None:
    """
    Configures the logger for script execution.

    This function sets the basic configuration for the logger,
    registers a function that returns 0 as the current virtual time,
    and sets the logger's level to NOTSET, which means that all messages will be processed.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(vtime)03dms] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    register_virtual_time_func(lambda: 0)
    logger.setLevel(logging.NOTSET)


F = TypeVar("F", bound=Callable[..., Any])


def rpc_call(func: F) -> F:
    """Decorator for making a remote procedure call (RPC).

    This decorator logs the function name and its arguments, executes the function,
    and handles any exceptions that occur during the function execution.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.
    """

    @functools.wraps(func)  # type: ignore
    def wrapper_rpc_call(*args, **kwargs):
        """Wrapper function for the RPC call.

        This function logs the function name and its arguments, executes the function,
        and handles any exceptions that occur during the function execution.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the function execution.

        Raises:
            Exception: If an error occurs during the function execution.
        """
        fields = [(desc.name, str(val).strip()) for desc, val in args[1].ListFields()]
        logger.debug(f"[gRPC]: {func.__name__}: {fields}")
        try:
            return func(*args, **kwargs)
        except Exception as err:
            logger.fatal(f"gRPC call failed with: {err}")
            logger.fatal(traceback.format_exc())
            raise err

    return cast(F, wrapper_rpc_call)


def measure_duration(func: F) -> F:
    """Decorator for measuring the duration of a function call.

    This decorator logs the function name, its return value, and the duration of the function execution
    if the duration exceeds 500 microseconds. It also handles any exceptions that occur during the function execution.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.
    """

    @functools.wraps(func)  # type: ignore
    def wrapper_func(*args, **kwargs):
        """Wrapper function for measuring the duration.

        This function logs the function name, its return value, and the duration of the function execution
        if the duration exceeds 500 microseconds.
        It also handles any exceptions that occur during the function execution.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the function execution.

        Raises:
            Exception: If an error occurs during the function execution.
        """
        try:
            start_time = time.monotonic_ns()
            result = func(*args, **kwargs)
            duration = time.monotonic_ns() - start_time
            if duration > 500_000:  # 500 microseconds
                logger.debug(
                    f"Function call ({func.__name__} returning {result})took: {duration * 1e-3:.2f} microsecs"
                )
            return result
        except Exception as err:
            logger.fatal(f"gRPC call failed with: {err}")
            logger.fatal(traceback.format_exc())
            raise err

    return cast(F, wrapper_func)
