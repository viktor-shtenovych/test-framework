import dataclasses
import struct

import bitstruct


@dataclasses.dataclass
class ConfigurationMsg310:
    """
    Footswitch Configuration – CAN ID 310h.
    """

    newest_supported_proto_version: int = 255
    oldest_supported_proto_version: int = 1
    channel_number: int = 10
    modem_tx_power_attenuation: int = 0
    console_network_id: int = 0
    pairing_info_valid: bool = True
    console_type: int = 1
    modem_tx_power_level: int = 1

    def pack(self) -> bytes:
        """
        Method returning the Configuration Info.

        Args:
            self: raw data packet from can communications

        Returns:
            Newest Supported Protocol Version
            Oldest Supported Protocol Version
            Network Channel Number
            Modem Transmit Power Attenuation
            Console Network ID
            Pairing Information Valid
            Console Type
            Modem Transmit Power Level
        """
        byte6 = bitstruct.pack(">p5u2b1", self.console_type, self.pairing_info_valid)

        return struct.pack(
            "BBBBhsB",
            self.newest_supported_proto_version,
            self.oldest_supported_proto_version,
            self.channel_number,
            self.modem_tx_power_attenuation,
            self.console_network_id,
            byte6,
            self.modem_tx_power_level,
        )


@dataclasses.dataclass
class ConfigurationMsg311:
    """
    Footswitch Configuration – CAN ID 311h.
    """

    detent_position_2: int = 50
    battery_charging_disable: bool = False
    detent_position_1: int = 15
    vibrate_on_down_enable: bool = True
    detent_strength: int = 0

    def pack(self) -> bytes:
        """
        Method returning the Configuration Info.

        Args:
            self: raw data packet from can communications

        Returns:
            Detent Position 2
            Battery Charging Disable
            Detent Position 1
            Vibrate On Down Enable
            Detent Strength
        """
        byte0: bytes = bitstruct.pack(
            ">b1u7", self.battery_charging_disable, self.detent_position_2
        )
        byte1: bytes = bitstruct.pack(
            ">b1u7", self.vibrate_on_down_enable, self.detent_position_1
        )
        byte2: bytes = struct.pack("B", self.detent_strength)
        byte3_7: bytes = b"\x00" * 5  # Unused bytes, set to zero

        return byte0 + byte1 + byte2 + byte3_7
