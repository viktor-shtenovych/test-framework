from datetime import datetime
import os
import threading
from typing import Iterator, Type, TypeVar
import _pytest.fixtures

from framework.support.reports import logger, log
from framework.simulators.base_simulator import BaseSimulator
from framework.support.vtime import vtime_manager
from framework.support.vtime import get_worker_manager, VirtualTimeWorker
from framework.support.py_emulator.sut_control import SutControl

TCP_PORT_ARG_NAME = "--rpc-port"

T = TypeVar("T", bound=BaseSimulator)


def is_execution_distributed() -> bool:
    """
    Check if the test is running in a distributed environment.
    """
    return bool("PYTEST_XDIST_TESTRUNUID" in os.environ)


def get_rpc_port(request: _pytest.fixtures.FixtureRequest) -> int:
    """
    Get the RPC port from the command line arguments.
    """
    if is_execution_distributed():
        return 0
    return int(request.config.getoption(TCP_PORT_ARG_NAME))


def create_simulator(
    request: _pytest.fixtures.FixtureRequest,
    simulator_cls: Type[T],
) -> Iterator[T]:
    """
    Create a simulator.
    """
    log.register_virtual_time_func(vtime_manager.time_ms)
    get_worker_manager().register_worker(VirtualTimeWorker.current_worker())
    sim = simulator_cls(get_rpc_port(request))
    sim.run()
    yield sim
    get_worker_manager().unregister_worker(VirtualTimeWorker.current_worker())
    sim.stop()


def create_emulator(
    request: _pytest.fixtures.FixtureRequest, simulator: BaseSimulator
) -> Iterator[None]:
    """
    Create an emulator.

    Args:
        request: Pytest fixture request object.
        simulator: Base simulator object.

    Returns:
        Simulator object fixture.
    """

    def emu_close_request_cb() -> threading.Event:
        simulator.irq_manager.raise_interrupt(-15)
        return simulator.rpc_connect_svc.get_closed_event()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    emu_log_file_pathname = os.path.abspath(
        os.path.join(
            __file__, f"..//..//emulator_{request.node.name}_{timestamp}_log.txt"
        )
    )
    cmd = request.config.getoption("--emulator")
    emulator = SutControl(
        emulator_cmd_line=cmd,
        emu_close_req_cb=emu_close_request_cb,
        log_file_pathname=emu_log_file_pathname if cmd is not None else "",
        emu_rpc_port=int(simulator.port),
    )
    if cmd is not None:
        emulator.start()
    else:
        logger.info("Waiting for emulator connection")
    simulator.wait_for_initialization()
    yield
    emulator.stop(try_gracefully=True)
