from typing import Callable

from framework.hardware_interfaces.drivers.common.connect import Connect
from framework.hardware_interfaces.drivers.common.flexcan_driver import FlexCanDriver
from framework.hardware_interfaces.drivers.common.definitions.mcu_types import MCUType
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    TInterruptCallback,
    TimerManagerABC,
    PITChannelManagerABC,
    BaseSifDriver,
    BasePinDriver,
)
from framework.hardware_interfaces.drivers.common.async_interface_driver import (
    AsyncInterfaceDriver,
)
from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_emios_common_driver import (
    EmiosCommonDriver,
)
from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_emios_mc_driver import (
    EmiosMcDriver,
)
from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_emios_qdec_driver import (
    EmiosQdecDriver,
)
from framework.hardware_interfaces.drivers.mpc5777c.etpu_i2c_driver import EtpuI2cDriver
from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_eqadc_driver import (
    EqAdcDriver,
)
from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_mcan_driver import (
    MCANDriver,
)
from framework.hardware_interfaces.drivers.mpc5777c.pit_driver import PitDriver
from framework.hardware_interfaces.drivers.s32k148.pwm_driver import PwmDriver
from framework.hardware_interfaces.drivers.s32k148.lpit_driver import LpitDriver
from framework.hardware_interfaces.drivers.s32k148.rtc_driver import RtcDriver
from framework.hardware_interfaces.drivers.s32k148.ftm_driver import FtmDriver

from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_sif_driver import (
    SifDriver as Mpc5777cSifDriver,
)
from framework.hardware_interfaces.drivers.mpc5777c.mpc5777c_pins_driver import (
    PinDriver as Mpc5777cPinDriver,
)
from framework.hardware_interfaces.drivers.s32k148.s32k148_sif_driver import (
    SifDriver as S32k148SifDriver,
)
from framework.hardware_interfaces.drivers.s32k148.s32k148_pins_driver import (
    PinDriver as S32k148PinDriver,
)


def get_etpu_i2c_drv(raise_interrupt_func: Callable[[int, int], None]) -> EtpuI2cDriver:
    """
    ! Get the ETPU I2C driver.
    """
    return EtpuI2cDriver(raise_interrupt_func)


def get_emios_qdec_drv(
    raise_interrupt_func: TInterruptCallback | None,
) -> EmiosQdecDriver:
    """
    ! Get the EMIOS driver for QDEC.
    """
    return EmiosQdecDriver(raise_interrupt_func)


def get_emios_mc_drv(raise_interrupt_func: TInterruptCallback | None) -> EmiosMcDriver:
    """
    ! Get the EMIOS driver for MC.
    """
    return EmiosMcDriver(raise_interrupt_func)


def get_emios_common_drv(
    raise_interrupt_func: TInterruptCallback | None,
) -> EmiosCommonDriver:
    """
    ! Get the EMIOS common driver.
    """
    return EmiosCommonDriver(raise_interrupt_func)


def get_can_bus_drv(
    raise_interrupt_func: Callable[[int, int], None],
) -> FlexCanDriver:
    """
    ! Get the CAN bus driver.
    """
    return FlexCanDriver(raise_interrupt_func)


def get_mcan_drv(
    raise_interrupt_func: Callable[[int, int], None],
) -> MCANDriver:
    """
    ! Get the MCAN driver.
    """
    return MCANDriver(raise_interrupt_func)


def get_eqadc_drv(raise_interrupt_func: TInterruptCallback) -> EqAdcDriver:
    """
    ! Get the EQADC driver.
    """
    return EqAdcDriver(raise_interrupt_func)


def get_pins_drv(
    raise_interrupt_func: TInterruptCallback, mcu_type: MCUType
) -> BasePinDriver:
    """
    ! Get the pins driver based on the MCU type.
    """
    if mcu_type == MCUType.S32K148:
        return S32k148PinDriver(raise_interrupt_func)
    elif mcu_type == MCUType.MPC5777C:
        return Mpc5777cPinDriver(raise_interrupt_func)
    raise ValueError(f"Unsupported MCU type: {mcu_type}")


def get_lpit_drv(
    raise_interrupt_func: TInterruptCallback, timer_manger: TimerManagerABC
) -> LpitDriver:
    """
    ! Get the LPIT driver.
    """
    return LpitDriver(raise_interrupt_func, timer_manger)


def get_ftm_drv() -> FtmDriver:
    """
    ! Get the FTM driver.
    """
    return FtmDriver()


def get_sync_drv(
    raise_interrupt_func: TInterruptCallback, mcu_type: MCUType
) -> BaseSifDriver:
    """
    ! Get the SIF driver.
    """
    if mcu_type == MCUType.S32K148:
        return S32k148SifDriver(raise_interrupt_func)
    elif mcu_type == MCUType.MPC5777C:
        return Mpc5777cSifDriver(raise_interrupt_func)
    raise ValueError(f"Unsupported MCU type: {mcu_type}")


def get_pwm_drv() -> PwmDriver:
    """
    ! Get the PWM driver.
    """
    return PwmDriver()


def get_rtc_drv(raise_interrupt_func: TInterruptCallback) -> RtcDriver:
    """
    ! Get the RTC driver.
    """
    return RtcDriver(raise_interrupt_func)


def get_rpc_connect() -> Connect:
    """
    ! Get the RPC connect.
    """
    return Connect()


def get_async_drv(
    raise_interrupt_func: Callable[[int, int], None],
) -> AsyncInterfaceDriver:
    """
    ! Get the async interface driver.
    """
    return AsyncInterfaceDriver(raise_interrupt_func)


def get_pit_drv(
    raise_interrupt_func: TInterruptCallback, timer_manager: PITChannelManagerABC
) -> PitDriver:
    """
    ! Get the PIT driver.
    """
    return PitDriver(raise_interrupt_func, timer_manager)
