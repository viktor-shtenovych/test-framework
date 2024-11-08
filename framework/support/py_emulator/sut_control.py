import subprocess
import sys
import threading
from typing import Any, Callable

from framework.support.reports import logger


class SutControl:
    """Support for starting/stopping of SW-under-test."""

    def __init__(
        self,
        emulator_cmd_line: str,
        emu_close_req_cb: Callable[[], threading.Event],
        log_file_pathname: str,
        emu_rpc_port: int,
    ) -> None:
        self.cmd_line = emulator_cmd_line
        self.process: subprocess.Popen[Any] | None = None
        self._log_file_pathname = log_file_pathname
        self._emu_close_req_cb = emu_close_req_cb
        self._emu_rpc_port = emu_rpc_port

    def start(self) -> None:
        """
        Start emulator.

        Raises:
            RuntimeError: If emulator stopped unexpectedly.
        """
        logger.info(f"Starting emulator `{self.cmd_line}`, port: {self._emu_rpc_port}.")
        cmd_line_list = self.cmd_line.split()

        if cmd_line_list[0] == "python":
            # Use python interpreter for running emulator.
            # use the one from current env
            cmd_line_list[0] = sys.executable

        cmd_line_list.extend(
            [f"localhost:{self._emu_rpc_port}", f"{self._log_file_pathname}"]
        )

        self.process = subprocess.Popen(
            cmd_line_list, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # Check if process does not stop immediately
        try:
            self.process.wait(1)

            # Process is terminated
            stdout = (
                self.process.stdout.read().decode("utf-8")
                if self.process.stdout
                else ""
            )
            stderr = (
                self.process.stderr.read().decode("utf-8")
                if self.process.stderr
                else ""
            )
            raise RuntimeError(f"Emulator stopped unexpectedly: \n{stdout}\n{stderr}")
        except subprocess.TimeoutExpired:
            # Process is still running. This is expected
            pass

    def stop(self, try_gracefully: bool = True) -> None:
        """
        Stop emulator.

        Args:
            try_gracefully: If True, try to close emulator gracefully.
        """
        is_closed_gracefully = False
        if try_gracefully:
            logger.info("Stopping emulator gracefully")
            closed_event: threading.Event = self._emu_close_req_cb()
            if closed_event.wait(3):
                # Emulator reported about closing itself
                is_closed_gracefully = True
                # If emulator is a child process (not separatelly opened)
                if self.process is not None:
                    try:
                        # Wait for emulator to close itself
                        self.process.wait(timeout=3)
                        logger.info("Emulator stopped gracefully")
                    except subprocess.TimeoutExpired:
                        # If emulator not closed itself for some reason
                        is_closed_gracefully = False

        if (self.process is not None) and (not is_closed_gracefully):
            logger.info("Stopping emulator forcefully")
            self.process.kill()
            self.process.wait(timeout=3)
            logger.info("Emulator stopped forcefully")
            self.process = None

        if len(self._log_file_pathname):
            logger.info(f"Emulator output saved in {self._log_file_pathname}")
        else:
            logger.info("Emulator output saved in emulator repository folder")
