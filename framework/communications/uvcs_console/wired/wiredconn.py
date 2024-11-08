from typing import Callable, Type, TypeAlias, TypeVar, cast, Protocol

from framework.communications.uvcs_footswitch.msg_types.configuration_msg import (
    ConfigurationMsg311,
    ConfigurationMsg310,
)
from framework.communications.uvcs_footswitch.msg_types.fault_msgs import (
    Fault010,
    Fault011,
)
from framework.communications.uvcs_footswitch.msg_types.real_time_status_msgs import (
    StatusMsg210,
    StatusMsg211,
    StatusMsg212,
)
from framework.support.reports import logger
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    CanBus,
    CanMessage,
)
from framework.support.vtime import vtime_manager
from framework.communications.uvcs_footswitch.msg_types.level_sensor_controller import (
    BarcodeReaderScanReply,
)

Msg: TypeAlias = (
    StatusMsg210
    | StatusMsg211
    | StatusMsg212
    | Fault010
    | Fault011
    | BarcodeReaderScanReply
)
TxMsg: TypeAlias = ConfigurationMsg310 | ConfigurationMsg311
MsgT = TypeVar("MsgT", bound=Msg)


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


class WiredConn:
    """
    Class implementing to support for uvcs_footswitch communication.

    The protocol defined in `UVCS Console Software Communication
    Specification - Footswitch` section `Controller Area Network (CAN) – Footswitch`
    """

    def __init__(self, bus: CanBus):
        self._bus = bus

    def send_config(self, message: TxMsg) -> None:
        """
        Send the configuration message.

        Args:
            message (TxMsg): The configuration message.
        """
        if isinstance(message, ConfigurationMsg310):
            can_msg = CanMessage(arbitration_id=0x310, data=message.pack())
        elif isinstance(message, ConfigurationMsg311):
            can_msg = CanMessage(arbitration_id=0x311, data=message.pack())
        else:
            raise AttributeError(f"Unknown configuration message: {message}")
        self._bus.send(can_msg)

    def _unpack_message(self, arbitration_id: int, data: bytes) -> Msg:
        """
        Unpack the message.

        Args:
            arbitration_id (int): The arbitration ID.
            data (bytes): The data.

        Returns:
            Msg: The message.
        """
        unpackers: dict[int, Type[Unpackable]] = {
            0x210: StatusMsg210,
            0x211: StatusMsg211,
            0x212: StatusMsg212,
            0x010: Fault010,
            0x011: Fault011,
        }
        try:
            message_cls = unpackers[arbitration_id]
            return cast(Msg, message_cls.unpack(data))
        except KeyError as err:
            raise AttributeError(f"Unknown message id: {arbitration_id} ({str(err)})")

    def _get_message(self, timeout: int | float = 0.1) -> Msg:
        """
        Get the message.

        Args:
            timeout (int | float, optional): The timeout. Defaults to 0.1.

        Returns:
            Msg: The message.
        """
        start_time = vtime_manager.time_ms()
        end_time = start_time + timeout * 1000
        while vtime_manager.time_ms() < end_time:
            msg = self._bus.recv(timeout=timeout)
            if msg:
                try:
                    foot_switch_msg = self._unpack_message(msg.arbitration_id, msg.data)
                    logger.debug(f"Received message: {foot_switch_msg}")
                    return foot_switch_msg
                except AttributeError as err:
                    logger.error(
                        f"Cannot parse message({msg.arbitration_id}) {msg.data.hex()} ({str(err)})."
                    )
        raise RuntimeError("No CAN message received")

    def await_message(
        self,
        filter_msg_type: Type[MsgT],
        filter_func: Callable[[MsgT], bool] | None = None,
        timeout: int | float = 0.5,
    ) -> MsgT:
        """
        Await a message.

        Args:
            filter_msg_type (Type[MsgT]): The message type.
            filter_func (Callable[[MsgT], bool], optional): The filter function. Defaults to None.
            timeout (int | float, optional): The timeout. Defaults to 0.5.

        Returns:
            MsgT: The message.
        """
        start_time = vtime_manager.time_ms()
        end_time = start_time + timeout * 1000
        while vtime_manager.time_ms() < end_time:
            message = self._get_message(timeout)
            if isinstance(message, filter_msg_type):
                if filter_func is None or filter_func(message):
                    return message
        raise CanMsgTimeoutError("Timeout waiting for CAN message")

    def _get_status(
        self,
        status_msg: Type[MsgT],
        filter_func: Callable[[MsgT], bool] | None = None,
        timeout: int | float = 0.5,
    ) -> MsgT:
        """
        Get the status.

        Args:
            status_msg (Type[MsgT]): The status message.
            filter_func (Callable[[MsgT], bool], optional): The filter function. Defaults to None.
            timeout (int | float, optional): The timeout. Defaults to 0.5.

        Returns:
            MsgT: The message.
        """
        return self.await_message(status_msg, filter_func, timeout)
