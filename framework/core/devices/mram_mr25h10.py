from framework.hardware_interfaces.drivers.s32k148.s32k148_sif_driver import (
    SynchronousIfDevice,
)
from enum import IntEnum


class Commands(IntEnum):
    """
    An enumeration to represent the commands for the MR25H10 MRAM.
    """

    READ = 0x03
    WRITE = 0x02
    WRITE_EN = 0x06
    WRITE_DIS = 0x04


class MramMr25h10(SynchronousIfDevice):
    """
    A class to represent the MR25H10 MRAM.

    Attributes:
        _cmd (Commands): The command for the MRAM.
        _addr (int): The address for the MRAM.
        _sim_data (list[int]): The simulated data for the MRAM.
        _write_en (bool): A flag to indicate whether the MRAM is in write mode.
    """

    def __init__(self, instance_id: int, address: int) -> None:
        super().__init__(instance_id, address)
        self._cmd = Commands.READ
        self._addr = 0
        self._sim_data: list[int] = [0xFF] * (128 * 1024)
        self._write_en = False

    def write_to_memory(self, addr: int, data: bytes) -> None:
        """
        Write data to the memory.

        Args:
            addr (int): The address to write the data to.
            data (bytes): The data to write to the memory.
        """
        for i in range(0, len(data)):
            self._sim_data[addr + i] = int(data[i])

    def read(self, size: int) -> bytes:
        """
        Read data from the memory.

        Args:
            size (int): The size of the data to read.

        Returns:
            bytes: The data read from the memory.
        """
        if self._cmd == Commands.READ:
            return bytes([0x00] * 4) + bytes(
                self._sim_data[self._addr : (self._addr + size - 4)]
            )
        else:
            return bytes([0xFF] * size)

    def write(self, data: bytes) -> None:
        """
        Write data to the memory.

        Args:
            data (bytes): The data to write to the memory.
        """
        self._cmd = Commands(data[0])
        if len(data) > 4:
            self._addr = (data[1] << 16) | (data[2] << 8) | data[3]
        if self._cmd == Commands.WRITE:
            if self._write_en:
                for i in range(0, len(data) - 4):
                    self._sim_data[self._addr + i] = data[i + 4]
        elif self._cmd == Commands.WRITE_EN:
            self._write_en = True
        elif self._cmd == Commands.WRITE_DIS:
            self._write_en = False
