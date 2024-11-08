from framework.communications.uvcs_console.wired.wiredconn import WiredConn
from typing import Callable, TypeAlias, TypeVar, Union, Optional

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
from framework.hardware_interfaces.drivers.common.definitions.interfaces import CanBus
from framework.support.vtime import VirtualTimeWorker, get_worker_manager, vtime_manager

Msg: TypeAlias = StatusMsg210 | StatusMsg211 | StatusMsg212 | Fault010 | Fault011
TxMsg: TypeAlias = ConfigurationMsg310 | ConfigurationMsg311
MsgT = TypeVar("MsgT", bound=Msg)


class FootSwitchCAN(WiredConn):
    """
    ! FootSwitchCAN communicates with the footswitch over the CAN bus.
    """

    def __init__(self, bus: CanBus) -> None:
        super().__init__(bus)
        self._enabling_beacons = False
        self._beacons_runner: VirtualTimeWorker | None = None

    def get_status_210(
        self,
        filter_func: Callable[[StatusMsg210], bool] | None = None,
        timeout: int | float = 0.5,
    ) -> StatusMsg210:
        """
        ! Get the status 210.

        @param filter_func The filter function. Defaults to None.
        @param timeout The timeout. Defaults to 0.5.
        @returns StatusMsg210: The status message.
        """
        return self._get_status(StatusMsg210, filter_func, timeout)

    def get_status_211(
        self,
        filter_func: Callable[[StatusMsg211], bool] | None = None,
        timeout: int | float = 0.5,
    ) -> StatusMsg211:
        """
        ! Get the status 211.

        @param filter_func The filter function. Defaults to None.
        @param timeout The timeout. Defaults to 0.5.
        @return StatusMsg211: The status message.
        """
        return self._get_status(StatusMsg211, filter_func, timeout)

    def get_status_212(
        self,
        filter_func: Callable[[StatusMsg212], bool] | None = None,
        timeout: int | float = 0.5,
    ) -> StatusMsg212:
        """
        ! Get the status 212.

        @param filter_func The filter function. Defaults to None.
        @param timeout The timeout. Defaults to 0.5.
        @return StatusMsg212: The status message.
        """
        return self._get_status(StatusMsg212, filter_func, timeout)

    def get_fault_msg010(
        self,
        filter_func: Callable[[Fault010], bool] | None = None,
        timeout: int | float = 0.5,
    ) -> Fault010:
        """
        ! Get the fault message 010.

        @param filter_func The filter function. Defaults to None.
        @param timeout The timeout. Defaults to 0.5.
        @return Fault010: The fault message.
        """
        return self._get_status(Fault010, filter_func, timeout)

    def get_fault_msg011(
        self,
        filter_func: Callable[[Fault011], bool] | None = None,
        timeout: int | float = 0.5,
    ) -> Fault011:
        """
        ! Get the fault message 011.

        @param filter_func The filter function. Defaults to None.
        @param timeout The timeout. Defaults to 0.5.
        @return Fault011: The fault message.
        """
        return self._get_status(Fault011, filter_func, timeout)

    def send_beacons(
        self,
        period: float,
        beacons: list[Union[ConfigurationMsg310, ConfigurationMsg311]],
    ) -> None:
        """
        ! Send beacons.

        @param period The period.
        @param beacons The beacons.
        """
        if beacons is None:
            self._enabling_beacons = False
        while self._enabling_beacons:
            for beacon in beacons:
                self.send_config(beacon)
            vtime_manager.sleep(period)

    def enable_beacons(
        self,
        period: float,
        beacons: Optional[list[Union[ConfigurationMsg310, ConfigurationMsg311]]],
    ) -> None:
        """
        ! Enable beacons.

        @param period The period.
        @param beacons The beacons.
        """
        self.disable_beacons()
        self._beacons_runner = VirtualTimeWorker(
            target=self.send_beacons,
            args=(period, beacons),
        )
        self._enabling_beacons = True
        self._beacons_runner.start()

    def disable_beacons(self) -> None:
        """
        ! Disable beacons.
        """
        self._enabling_beacons = False
        if self._beacons_runner is not None:
            get_worker_manager().go_idle(VirtualTimeWorker.current_worker())
            self._beacons_runner.join()
            get_worker_manager().go_active(VirtualTimeWorker.current_worker())
            self._beacons_runner = None
