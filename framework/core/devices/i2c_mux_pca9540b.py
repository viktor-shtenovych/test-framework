from framework.support.reports import logger
from framework.hardware_interfaces.drivers.s32k148.s32k148_sif_driver import (
    SynchronousIfDevice,
)


class I2CMuxPcs9540BData(SynchronousIfDevice):
    """
    I2C multiplexer data.
    """

    def __init__(
        self,
        instance_id: int,
        address: int,
        device1: SynchronousIfDevice,
        device2: SynchronousIfDevice,
    ):
        super().__init__(instance_id, address)
        self._device1 = device1
        self._device2 = device2
        self._selected = self._device1

    def switch(self, use_device1: bool) -> None:
        """
        Switch between the two devices.

        Args:
            use_device1: True to use device1, False to use device2.
        """
        device_str = "device1" if use_device1 else "device2"
        logger.debug(f"Start communication with i2c {device_str}")
        self._selected = self._device1 if use_device1 else self._device2

    def read(self, size: int) -> bytes:
        """
        Read data.

        Args:
            size: Number of bytes to read.
        """
        return self._selected.read(size)

    def write(self, data: bytes) -> None:
        """
        Write data.

        Args:
            data: Data to write.
        """
        self._selected.write(data)


class I2CMuxPca9540BControl(SynchronousIfDevice):
    """
    I2C multiplexer control.

    https://www.nxp.com/docs/en/data-sheet/PCA9540B.pdf
    """

    def __init__(self, instance_id: int, address: int, mux: I2CMuxPcs9540BData) -> None:
        super().__init__(instance_id, address)
        self._i2c_mux = mux

    def write(self, data: bytes, address: int | None = None) -> None:
        """
        Write data.

        Args:
            data: Data to write.
            address: Address of the device to write to.
        """
        if data == bytes([0x04]):
            self._i2c_mux.switch(use_device1=True)
        elif data == bytes([0x05]):
            self._i2c_mux.switch(use_device1=False)
        else:
            raise AttributeError(
                f"Wrong argument for ic2 device selection: {data.hex()}"
            )

    def read(self, size: int) -> bytes:
        """
        Read data.

        Args:
            size: Number of bytes to read.
        """
        raise NotImplementedError("No data reading ")
