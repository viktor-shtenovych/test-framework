"""! @Brief BaseSimulator class that initializes all the hardware drivers and gRPC server."""

#
# @file base_simulator.py
#
# @brief BaseSimulator class that initializes all the hardware drivers and gRPC server.
#
# @section description_base_simulator Description
# This module represents the BaseSimulator class.
#
# @section libraries_base_simulator Libraries/Modules
# - signal standard library
# - abc standard library
# - concurrent.futures standard library
# - grpc module
# - framework.core.control.encoder module (local)
#   - Access to Encoder class.
# - framework.support.reports module (local)
#   - Access to logger class.
# - framework.hardware_interfaces.drivers module (local)
#   - Access to get_rpc_connect function.
# - framework.hardware_interfaces.drivers.common.interrupts module (local)
#   - Access to Interrupts class.
#
# @section notes_base_simulator Notes
# - None.
#
# @section todo_base_simulator TODO
# - None.
#
# @section author_base_simulator Author(s)
# - Created by:
#   - Lubos Kocvara <lubos.kocvara@globallogic.com> on 26/04/2024.
# - Modified by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 09/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.
import signal
from abc import abstractmethod, ABC
from concurrent import futures

import grpc

from framework.core.control.encoder import Encoder
from framework.support.reports import (
    logger,
)
from framework.hardware_interfaces.drivers import (
    get_rpc_connect,
)

from framework.hardware_interfaces.drivers.common.interrupts import Interrupts


class BaseSimulator(ABC):
    """
    Simulator class that initializes all the hardware drivers and gRPC server.
    """

    def __init__(self, rpc_listening_port: int) -> None:
        # Allow interruption Ctrl+C
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Interrupt manager
        self.irq_manager = Interrupts()

        # HW drivers simulator
        self.rpc_connect_svc = get_rpc_connect()
        self.encoder = Encoder(self.irq_manager.raise_interrupt)
        # gRPC server setup
        self.port = str(rpc_listening_port)
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        self.port = self.server.add_insecure_port("[::]:" + self.port)

    def run(self) -> None:
        """
        Start the simulator.
        """
        self.server.start()
        self.irq_manager.start()
        logger.info(f"Server started, listening on {self.port}")

    def run_forever(self) -> None:
        """
        Start the simulator and wait for termination.
        """
        self.run()
        self.server.wait_for_termination()

    @abstractmethod
    def wait_for_initialization(self) -> None:
        """
        Wait for all the hardware drivers to initialize.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the simulator.

        This method stops the gRPC server and all the hardware drivers.
        """
        pass
