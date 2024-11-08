from typing import Type, TypeAlias, cast, Protocol, Callable
from framework.hardware_interfaces.drivers.common.definitions.interfaces import CanBus
from framework.communications.uvcs_footswitch.msg_types.level_sensor_controller import (
    BarcodeReaderScanReply as BarcodeReaderScanReply,
)
from framework.communications.uvcs_console.wired.wiredconn import WiredConn

Msg: TypeAlias = BarcodeReaderScanReply


class Unpackable(Protocol):
    """
    Protocol to define the unpack method.
    """

    @classmethod
    def unpack(cls, data: bytes) -> "Unpackable":
        """
        Unpack the data.
        """
        ...


class CanMsgTimeoutError(TimeoutError):
    """
    Class to represent a CAN message timeout error.
    """

    pass


class FluidicsCan(WiredConn):
    """
    Class to handle communication with Fluidics CAN.

    The protocol defined in `UVCS Console Software Communication
    Specification - Subsystem` section `Fluidics CAN`
    """

    def __init__(self, bus: CanBus):
        super().__init__(bus)

    def _unpack_message(self, arbitration_id: int, data: bytes) -> Msg:
        """
        Unpack the message.

        Args:
            arbitration_id (int): The arbitration ID.
            data (bytes): The data.

        Returns:
            Msg: The message.
        """
        unpackers: dict[int, Type[Unpackable]] = {0x1C1E0806: BarcodeReaderScanReply}
        try:
            message_cls = unpackers[arbitration_id]
            return cast(Msg, message_cls.unpack(data))
        except KeyError as err:
            raise AttributeError(f"Unknown message id: {arbitration_id} ({str(err)})")

    def get_barcode_reader_scan_reply(
        self,
        filter_func: Callable[[BarcodeReaderScanReply], bool] | None = None,
        timeout: int | float = 0.5,
    ) -> BarcodeReaderScanReply:
        """
        Get the status 210.

        Args:
            filter_func (Callable[[StatusMsg210], bool], optional): The filter function. Defaults to None.
            timeout (int | float, optional): The timeout. Defaults to 0.5.

        Returns:
            StatusMsg210: The status message.
        """
        return self._get_status(BarcodeReaderScanReply, filter_func, timeout)
