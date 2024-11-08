import functools
import threading
import concurrent.futures
from concurrent.futures import Future
from typing import TypeAlias, List, Callable, Any, TypeVar, ParamSpec

from framework.support.reports import logger

WorkerId: TypeAlias = int


class VirtualTimeWorker(threading.Thread):
    """Custom thread managed by virtual vtime."""

    OVERWRITE_PREFIX = "WORKERID"

    def run(self) -> None:
        """Run the thread. Notify worker manager about new working thread."""
        get_worker_manager().register_worker(self.current_worker())
        super().run()
        get_worker_manager().unregister_worker(self.current_worker())

    @staticmethod
    def current_worker() -> WorkerId:
        """
        Get ID of current worker. This is based on thread identifier.

        For workers running outside this framework (i.e. emulator) we can set the ID by setting specific prefix+ID
        in thread name - see `set_worker_id` decorating function.
        """
        if threading.current_thread().name.startswith(
            VirtualTimeWorker.OVERWRITE_PREFIX
        ):
            return WorkerId(
                threading.current_thread().name.removeprefix(
                    VirtualTimeWorker.OVERWRITE_PREFIX
                )
            )

        ident = threading.current_thread().ident
        assert ident is not None
        return ident

    @staticmethod
    def set_worker_id(func):  # type: ignore
        """
        Decorator used for methods executed from outside this framework.

        As the framework implementation of RPC may use multiple threads but still
        representing one emulator's thread this decorator set's thread name
        which is then used by `current_worker` method when getting worker ID.
        """

        @functools.wraps(func)  # type: ignore
        def wrapper_set_worker_id(obj, *args, **kwargs):
            orig_thread_name = threading.current_thread().name
            if hasattr(obj, "_worker_id"):
                threading.current_thread().name = (
                    f"{VirtualTimeWorker.OVERWRITE_PREFIX}{obj._worker_id}"
                )
            return_value = func(obj, *args, **kwargs)
            threading.current_thread().name = orig_thread_name
            return return_value

        return wrapper_set_worker_id


class WorkersManager:
    """
    Manages workers which are virtual-vtime related.

    It stores list of all workers and list of all idle workers.
    In case all workers are in idle state then VirtualTimeManager is notified.
    """

    def __init__(self) -> None:
        self._idle_workers: List[WorkerId] = []
        self._all_workers: List[WorkerId] = []
        self.all_idle = threading.Event()
        self._update_idle: Callable[[], None] | None = None
        self._idle_lock = threading.RLock()

    def register_idle_observer(self, callback: Callable[[], None]) -> None:
        """
        Register callback which is called when all workers are idle.

        Args:
            callback: Function called when all workers are idle.
        """
        self._update_idle = callback

    def register_worker(self, worker_id: WorkerId) -> None:
        """
        Register worker.

        Args:
            worker_id: ID of worker to register.
        """
        logger.debug(f"Registering worker {worker_id}")
        assert worker_id not in self._all_workers
        self._all_workers.append(worker_id)

    def unregister_worker(self, worker_id: WorkerId) -> None:
        """
        Unregister worker.

        Args:
            worker_id: ID of worker to unregister.
        """
        logger.debug(f"Unregistering worker {worker_id}")
        if worker_id in self._all_workers:
            self._all_workers.remove(worker_id)
        if worker_id in self._idle_workers:
            self._idle_workers.remove(worker_id)
        self._check_idle()

    def go_idle(self, worker_id: WorkerId) -> None:
        """
        Notify that worker is idle.

        Args:
            worker_id: ID of worker which is idle.
        """
        logger.debug(
            f"Worker {worker_id} idle ({set(self._all_workers) - set(self._idle_workers)}"
        )
        assert worker_id in self._all_workers
        with self._idle_lock:
            self._idle_workers.append(worker_id)
            logger.debug("appended")
            self._check_idle()
            logger.debug("checked")

    def go_active(self, worker_id: WorkerId) -> None:
        """
        Notify that worker is active.

        Args:
            worker_id: ID of worker which is active.
        """
        logger.debug(f"Worker {worker_id} active")
        if worker_id in self._idle_workers:
            self._idle_workers.remove(worker_id)

    def _check_idle(self) -> None:
        """
        Check if all workers are idle and notify VirtualTimeManager.

        If all workers are idle then VirtualTimeManager is notified.
        """
        if set(self._idle_workers) == set(self._all_workers):
            if self._update_idle:
                logger.debug("All workers are idle")
                self._update_idle()

    def get_num_of_workers(self) -> int:
        """Return number of registered workers."""
        return len(self._all_workers)


_worker_manager = WorkersManager()


def get_worker_manager() -> WorkersManager:
    """
    Get worker manager.
    """
    return _worker_manager


class VirtualTimeThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor):
    """
    ThreadPoolExecutor which notifies `WorkersManager` when a task is submitted for execution.
    """

    _T = TypeVar("_T")
    _P = ParamSpec("_P")

    def submit(
        self, __fn: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
    ) -> Future[_T]:
        """
        Submit task for execution.

        Args:
            __fn: Function to execute.
            args: Function arguments.
            kwargs: Function keyword arguments.

        Returns:
            future: Future object representing the task.
        """

        def time_managed_func() -> Any:
            """
            Function which wraps the submitted function.

            It registers worker before executing the function and unregisters it after.
            """
            get_worker_manager().register_worker(VirtualTimeWorker.current_worker())
            result = __fn(*args, **kwargs)
            get_worker_manager().unregister_worker(VirtualTimeWorker.current_worker())
            return result

        return super().submit(time_managed_func)
