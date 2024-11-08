from typing import cast, List, Dict
from enum import IntEnum

from framework.hardware_interfaces.drivers.s32k148.s32k148_sif_driver import (
    SynchronousIfDevice,
)
from framework.support.reports import logger
from framework.hardware_interfaces.drivers.common.definitions.interfaces import Access


class RegAddr(IntEnum):
    """
    An enumeration to represent the register addresses for the ADP8866 LED driver.
    """

    kRegMFDVID = 0x00
    kRegMDCR = 0x01
    kRegINT_STAT = 0x02
    kRegINT_EN = 0x03
    kRegISCOFF_SEL1 = 0x04
    kRegISCOFF_SEL2 = 0x05
    kRegGAIN_SEL = 0x06
    kRegLVL_SEL1 = 0x07
    kRegLVL_SEL2 = 0x08
    kRegPWR_SEL1 = 0x09
    kRegPWR_SEL2 = 0x0A
    kRegCFGR = 0x10
    kRegBLSEL = 0x11
    kRegBLFR = 0x12
    kRegBLMX = 0x13
    kRegISCC1 = 0x1A
    kRegISCC2 = 0x1B
    kRegISCT1 = 0x1C
    kRegISCT2 = 0x1D
    kRegOFFTIMER6 = 0x1E
    kRegOFFTIMER7 = 0x1F
    kRegOFFTIMER8 = 0x20
    kRegOFFTIMER9 = 0x21
    kRegISCF = 0x22
    kRegISC1 = 0x23
    kRegISC2 = 0x24
    kRegISC3 = 0x25
    kRegISC4 = 0x26
    kRegISC5 = 0x27
    kRegISC6 = 0x28
    kRegISC7 = 0x29
    kRegISC8 = 0x2A
    kRegISC9 = 0x2B
    kRegHB_SEL = 0x2C
    kRegISC6_HB = 0x2D
    kRegISC7_HB = 0x2E
    kRegISC8_HB = 0x2F
    kRegISC9_HB = 0x30
    kRegOFFTIMER6_HB = 0x31
    kRegOFFTIMER7_HB = 0x32
    kRegOFFTIMER8_HB = 0x33
    kRegOFFTIMER9_HB = 0x34
    kRegISCT_HB = 0x35
    kRegDELAY6 = 0x3C
    kRegDELAY7 = 0x3D
    kRegDELAY8 = 0x3E
    kRegDELAY9 = 0x3F


class LedMode(IntEnum):
    """
    An enumeration to represent the LED modes.
    """

    OFF = 0
    ON_SOLID = 1
    ON_BLINKING = 2


init_configurations = {
    RegAddr.kRegMDCR: 0x6C,  # Active Mode
    RegAddr.kRegCFGR: 0x10,  # D9 independent sinks
    RegAddr.kRegBLSEL: 0xFF,  # D1-D8 are independent sinks
    RegAddr.kRegISCC1: 0x04,  # D9 enabled
    RegAddr.kRegISCC2: 0xFF,  # D1-D8 are all enabled
}


class LedDriverADP8866(SynchronousIfDevice):
    """
    A class to represent the ADP8866 LED driver.
    """

    def __init__(self, instance_id: int, address: int) -> None:
        super().__init__(instance_id, address)

        self.registers: Dict[RegAddr, Dict[str, int | str]] = {
            RegAddr.kRegMFDVID: {"value": 0x53, "access": Access.R},  # MFDVID
            RegAddr.kRegMDCR: {"value": 0x00, "access": Access.RW},  # MDCR
            RegAddr.kRegINT_STAT: {"value": 0x00, "access": Access.RW},  # INT_STAT
            RegAddr.kRegINT_EN: {"value": 0x00, "access": Access.RW},  # INT_EN
            RegAddr.kRegISCOFF_SEL1: {
                "value": 0x00,
                "access": Access.RW,
            },  # ISCOFF_SEL1
            RegAddr.kRegISCOFF_SEL2: {
                "value": 0x00,
                "access": Access.RW,
            },  # ISCOFF_SEL2
            RegAddr.kRegGAIN_SEL: {"value": 0x00, "access": Access.RW},  # GAIN_SEL
            RegAddr.kRegLVL_SEL1: {"value": 0x00, "access": Access.RW},  # LVL_SEL1
            RegAddr.kRegLVL_SEL2: {"value": 0x00, "access": Access.RW},  # LVL_SEL2
            RegAddr.kRegPWR_SEL1: {"value": 0x00, "access": Access.RW},  # PWR_SEL1
            RegAddr.kRegPWR_SEL2: {"value": 0x00, "access": Access.RW},  # PWR_SEL2
            # 0x0B to 0x0F Reserved
            RegAddr.kRegCFGR: {"value": 0x00, "access": Access.RW},  # CFGR
            RegAddr.kRegBLSEL: {"value": 0x00, "access": Access.RW},  # BLSEL
            RegAddr.kRegBLFR: {"value": 0x00, "access": Access.RW},  # BLFR
            RegAddr.kRegBLMX: {"value": 0x00, "access": Access.RW},  # BLMX
            # 0x14 to 0x19Reserve
            RegAddr.kRegISCC1: {"value": 0x00, "access": Access.RW},  # ISCC1
            RegAddr.kRegISCC2: {"value": 0x00, "access": Access.RW},  # ISCC2
            RegAddr.kRegISCT1: {"value": 0x00, "access": Access.RW},  # ISCT1
            RegAddr.kRegISCT2: {"value": 0x00, "access": Access.RW},  # ISCT2
            RegAddr.kRegOFFTIMER6: {"value": 0x00, "access": Access.RW},  # OFFTIMER6
            RegAddr.kRegOFFTIMER7: {"value": 0x00, "access": Access.RW},  # OFFTIMER7
            RegAddr.kRegOFFTIMER8: {"value": 0x00, "access": Access.RW},  # OFFTIMER8
            RegAddr.kRegOFFTIMER9: {"value": 0x00, "access": Access.RW},  # OFFTIMER9
            RegAddr.kRegISCF: {"value": 0x00, "access": Access.RW},  # ISCF
            RegAddr.kRegISC1: {"value": 0x00, "access": Access.RW},  # ISC1
            RegAddr.kRegISC2: {"value": 0x00, "access": Access.RW},  # ISC2
            RegAddr.kRegISC3: {"value": 0x00, "access": Access.RW},  # ISC3
            RegAddr.kRegISC4: {"value": 0x00, "access": Access.RW},  # ISC4
            RegAddr.kRegISC5: {"value": 0x00, "access": Access.RW},  # ISC5
            RegAddr.kRegISC6: {"value": 0x00, "access": Access.RW},  # ISC6
            RegAddr.kRegISC7: {"value": 0x00, "access": Access.RW},  # ISC7
            RegAddr.kRegISC8: {"value": 0x00, "access": Access.RW},  # ISC8
            RegAddr.kRegISC9: {"value": 0x00, "access": Access.RW},  # ISC9
            RegAddr.kRegHB_SEL: {"value": 0x00, "access": Access.RW},  # HB_SEL
            RegAddr.kRegISC6_HB: {"value": 0x00, "access": Access.RW},  # ISC6_HB
            RegAddr.kRegISC7_HB: {"value": 0x00, "access": Access.RW},  # ISC7_HB
            RegAddr.kRegISC8_HB: {"value": 0x00, "access": Access.RW},  # ISC8_HB
            RegAddr.kRegISC9_HB: {"value": 0x00, "access": Access.RW},  # ISC9_HB
            RegAddr.kRegOFFTIMER6_HB: {
                "value": 0x00,
                "access": Access.RW,
            },  # OFFTIMER6_HB
            RegAddr.kRegOFFTIMER7_HB: {
                "value": 0x00,
                "access": Access.RW,
            },  # OFFTIMER7_HB
            RegAddr.kRegOFFTIMER8_HB: {
                "value": 0x00,
                "access": Access.RW,
            },  # OFFTIMER8_HB
            RegAddr.kRegOFFTIMER9_HB: {
                "value": 0x00,
                "access": Access.RW,
            },  # OFFTIMER9_HB
            RegAddr.kRegISCT_HB: {"value": 0x00, "access": Access.RW},  # ISCT_HB
            # 0x36 to 0x3B Reserved
            RegAddr.kRegDELAY6: {"value": 0x00, "access": Access.RW},  # DELAY6
            RegAddr.kRegDELAY7: {"value": 0x00, "access": Access.RW},  # DELAY7
            RegAddr.kRegDELAY8: {"value": 0x00, "access": Access.RW},  # DELAY8
            RegAddr.kRegDELAY9: {"value": 0x00, "access": Access.RW},  # DELAY9
        }

        self.__init_config()

    def __init_config(self) -> None:
        """
        Initialize the configuration of the LED driver.
        """
        for reg_addr, reg_value in init_configurations.items():
            if reg_addr in self.registers:
                self.registers[reg_addr]["value"] = reg_value

    def read(self, size: int) -> bytes:
        """
        Read data from the LED driver.

        Args:
            size (int): The number of bytes to read.

        Returns:
            bytes: The data read from the LED driver.
        """
        logger.debug(
            f"LED driver Read: {size} bytes from register {self._register_address:02X}"
        )
        if self._register_address in self.registers and size == 1:
            data = cast(List[int], self.registers[self._register_address]["value"])
            return bytes(data[:size])
        else:
            # Handle reading from undefined registers by returning zeros
            return bytes([0x00] * size)

    def write(self, data: bytes) -> None:
        """
        Write data to the LED driver.

        Args:
            data (bytes): The data to write to the LED driver.
        """
        self._register_address = RegAddr(data[0])
        if len(data) > 1:
            logger.debug(
                f"LED driver Write: {data.hex()} to register {self._register_address:02X}"
            )

            if (
                self._register_address in self.registers
                and self.registers[self._register_address]["access"] == Access.RW
            ):
                self.registers[self._register_address]["value"] = data[1]

    def get_led_mode(self, channel: int) -> LedMode:
        """
        Get the mode of the LED.

        Args:
            channel (int): The channel number of the LED.

        Returns:
            LedMode: The mode of the LED.
        """
        assert (channel >= 1) and (channel <= 9)

        isc_reg_addr = RegAddr(RegAddr.kRegISC1 + channel - 1)
        if self.registers[isc_reg_addr]["value"] == 0:
            return LedMode.OFF
        else:
            off_timer = None
            if 1 <= channel <= 4:
                off_timer = (
                    cast(int, self.registers[RegAddr.kRegISCT2]["value"])
                    >> ((channel - 1) * 2)
                ) & 0x03
            elif channel == 5:
                off_timer = cast(int, self.registers[RegAddr.kRegISCT1]["value"]) & 0x03
            elif 6 <= channel <= 9:
                off_timer_reg_addr = RegAddr(RegAddr.kRegOFFTIMER6 + (channel - 6))
                off_timer = cast(int, self.registers[off_timer_reg_addr]["value"])

            if off_timer == 0:
                return LedMode.ON_SOLID
            else:
                return LedMode.ON_BLINKING
