from enum import IntEnum, Enum


class Ports(IntEnum):
    """
    ! Ports for the GPIO pins.
    """

    PORT_A = 0x40049000
    PORT_B = 0x4004A000
    PORT_C = 0x4004B000
    PORT_D = 0x4004C000
    PORT_E = 0x4004D000


class InputPins(Enum):
    """
    ! Input pins for the GPIO.
    """

    RIGHT_VERTICAL = (Ports.PORT_E, 13)
    RIGHT_HORIZONTAL = (Ports.PORT_E, 10)
    LEFT_VERTICAL = (Ports.PORT_E, 7)
    LEFT_HORIZONTAL = (Ports.PORT_E, 24)
    LEFT_HEEL = (Ports.PORT_E, 5)
    RIGHT_HEEL = (Ports.PORT_E, 9)

    TREADLE_UP0 = (Ports.PORT_E, 8)
    TREADLE_UP1 = (Ports.PORT_E, 12)
    TREADLE_UP2 = (Ports.PORT_E, 14)
    TREADLE_UP3 = (Ports.PORT_E, 0)
    TREADLE_UP4 = (Ports.PORT_E, 1)

    CABLE_IN = (Ports.PORT_A, 9)
    VCHGDT = (Ports.PORT_B, 20)
    VCOIL_PG = (Ports.PORT_B, 18)
    COIL_MON = (Ports.PORT_D, 13)

    BROKEN_SPR = (Ports.PORT_E, 25)

    PD_SHROUD_UP1 = (Ports.PORT_A, 30)
    PD_SHROUD_UP2 = (Ports.PORT_C, 3)
    BL654_BUSY = (Ports.PORT_A, 16)
    BL654_READY_N = (Ports.PORT_B, 8)
    BL654_TX = (Ports.PORT_B, 12)

    LATCH_CLOSED = (Ports.PORT_A, 139)
    LATCH_EJECT = (Ports.PORT_A, 137)


class OutputPins(Enum):
    """
    ! Output pins for the GPIO.
    """

    LED_SYSTEM = (Ports.PORT_D, 17)
    CHARGE_BATTERY1 = (Ports.PORT_B, 22)
    CHARGE_BATTERY2 = (Ports.PORT_B, 23)

    DETENT_EN = (Ports.PORT_C, 11)

    PLED_SHDUP_EN1 = (Ports.PORT_A, 31)
    PLED_SHDUP_EN2 = (Ports.PORT_D, 5)

    ETH_RST_N = (Ports.PORT_A, 245)
    FPGA_RST_N = (Ports.PORT_A, 257)
