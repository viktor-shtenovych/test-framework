"""CAN Communications Tests."""

from typing import cast, List

import pytest
from framework.communications.uvcs_footswitch.msg_types.aux_data_types import (
    AuxDataType,
    FootSwitchSwVersion,
)
from framework.communications.uvcs_footswitch.msg_types.configuration_msg import (
    ConfigurationMsg310,
    ConfigurationMsg311,
)
from framework.apps.footswitch import FootSwitch
from framework.support.reports import report
from framework.communications.uvcs_footswitch.msg_types.msg_data_structures import (
    FootSwitchType,
    FootSwitchState,
)
from tests.footswitch_tests.utils import (
    connect_footswitch_to_console,
    are_treadle_and_buttons_active,
)

BEACONS: list[ConfigurationMsg310 | ConfigurationMsg311] = [
    ConfigurationMsg310(),
    ConfigurationMsg311(),
]


class TestCanCommunications:
    """
    Test cases for CAN communications.
    """

    @staticmethod
    def examine_auxiliary_data_type(aux_data_messages: List[int]) -> bool:
        """
        Examine the auxiliary data type.

        Args:
            aux_data_messages: A list of auxiliary data messages.
        """
        result = True
        for sample in range(1, len(aux_data_messages)):
            if aux_data_messages[sample] != aux_data_messages[sample - 1] + 1:
                if (
                    aux_data_messages[sample - 1] != 31
                    or aux_data_messages[sample] != 0
                ):
                    result = False
        return result

    @staticmethod
    def beacons_enabled(foot_switch: FootSwitch) -> bool:
        """
        Check if the beacons are enabled.
        """
        start_time = foot_switch.vtime.time_ms()
        end_time = foot_switch.vtime.time_ms()
        beacon_status = True

        while end_time - start_time < 3_000:
            end_time = foot_switch.vtime.time_ms()
            try:
                message_210 = foot_switch.wired_conn.get_status_210()
                assert message_210 is not None, "Failed to receive StatusMsg210 message"

                message_211 = foot_switch.wired_conn.get_status_211()
                assert message_211 is not None, "Failed to receive StatusMsg211 message"

                message_212 = foot_switch.wired_conn.get_status_212()
                assert message_212 is not None, "Failed to receive StatusMsg212 message"

            except TimeoutError:
                assert end_time - start_time == pytest.approx(2000, abs=100)
                beacon_status = False
                return beacon_status

        return beacon_status

    @staticmethod
    def monitor_uart_tx(foot_switch: FootSwitch) -> bool:
        """
        Monitor UART1_TX.
        """
        start_time = foot_switch.vtime.time_ms()
        end_time = foot_switch.vtime.time_ms()
        foot_switch.modem.write_flag = False

        while end_time - start_time < 3_000:
            end_time = foot_switch.vtime.time_ms()
            foot_switch.vtime.sleep(0.2)
            if foot_switch.modem.write_flag:
                return True
        return False

    def test_status_report(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0120].
        """
        with report.TestStep("Cable Footswitch to Console and select.") as step:
            foot_switch_state, message = connect_footswitch_to_console(foot_switch)

            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                foot_switch_state,
                comment=f"Status message: {message}",
            )

        with report.TestStep("Verify that the treadle and buttons are active") as step:
            orientation_status, treadle_status, button_status = (
                are_treadle_and_buttons_active(foot_switch)
            )
            step.verify_equal(
                "Verify that the Footswitch is horizontally oriented",
                True,
                orientation_status,
            )
            step.verify_equal(
                "Verify that the treadle is active",
                True,
                treadle_status,
            )
            step.verify_equal(
                "Verify that the buttons are active",
                True,
                button_status,
            )

        with report.TestStep(
            "Record the value displayed in the field"
            "'WirelessFootswitchMajorVersion',"
            "'WirelessFootswitchMinorVersion' and"
            "'WirelessFootswitchDevVersion',"
            "on 'FswDiagAprdWirelessFswInfo' message view: ________________________."
        ) as step:
            message_211 = foot_switch.wired_conn.get_status_211(
                lambda x: x.aux_type == AuxDataType.FootSwitchSwVersion
            )
            message_211.data = cast(FootSwitchSwVersion, message_211.data)
            # Questions: What should be the software versions?
            step.verify_equal(
                "Verify WirelessFootswitchMajorVersion",
                0,
                message_211.data.major_version,
            )
            step.verify_equal(
                "Verify WirelessFootswitchMinorVersion",
                0,
                message_211.data.minor_version,
            )
            step.verify_equal(
                "Verify WirelessFootswitchDevVersion",
                0,
                message_211.data.development_version,
            )

        with report.TestStep("Monitor TP100 (BL654_UART1_TX/ Wireless Tx)."):
            step.verify_equal(
                "No communication on UART1_TX",
                False,
                self.monitor_uart_tx(foot_switch),
            )

    def test_record_timestamps(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0121].
        """
        with report.TestStep("Cable Footswitch to CANoe") as step:
            foot_switch_state, message = connect_footswitch_to_console(foot_switch)

            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                foot_switch_state,
                comment=f"Status message: {message}",
            )

        with report.TestStep(
            "Start CANoe with periodic transmission of CAN beacons disabled (CAN ID 0x310 and CAN ID 0x 311)"
        ) as step:
            message_210 = foot_switch.wired_conn.get_status_210()

            message_211 = foot_switch.wired_conn.get_status_211(
                lambda x: x.aux_type == AuxDataType.FootSwitchId
            )

            message_212 = foot_switch.wired_conn.get_status_212()

            step.verify_equal(
                "The connection as Cabled.",
                FootSwitchType.Centurion,
                message_210.foot_switch_state,
                comment=f"Footswitch type: {message_210.foot_switch_state}",
            )

            step.verify_equal(
                "Footswitch ID",
                1,
                message_211.aux_type.FootSwitchId,
                comment=f"Footswitch ID: {message_211.aux_type.FootSwitchId}",
            )

            step.verify_equal(
                "Newest Supported Protocol Version",
                1,
                message_212.newest_supported_proto_version,
                comment=f"Newest Supported Protocol Version: {message_212.newest_supported_proto_version}",
            )

            step.verify_equal(
                "Oldest Supported Protocol Version",
                1,
                message_212.oldest_supported_proto_version,
                comment=f"Oldest Supported Protocol Version: {message_212.oldest_supported_proto_version}",
            )

        with report.TestStep(
            "Enable periodic transmission of CAN beacons (CAN ID 0x310 and CAN ID 0x311 every 80ms) using CANoe."
        ) as step:
            foot_switch.wired_conn.enable_beacons(0.08, beacons=BEACONS)
            step.verify_equal(
                "The Beacons are enabled",
                True,
                self.beacons_enabled(foot_switch),
            )

        with report.TestStep(
            "Randomly pick three triples of status packets (CAN IDs 0x210, 0x211 and 0x212) and record their timestamps"
        ) as step:
            samples = 3
            timestamps_210 = []
            timestamps_211 = []
            timestamps_212 = []

            for _ in range(samples):
                foot_switch.wired_conn.get_status_210()
                timestamps_210.append(foot_switch.vtime.time_ms())

                foot_switch.wired_conn.get_status_211()
                timestamps_211.append(foot_switch.vtime.time_ms())

                foot_switch.wired_conn.get_status_212()
                timestamps_212.append(foot_switch.vtime.time_ms())

            packets_210_time_diffs = [
                timestamp2 - timestamp1
                for timestamp1, timestamp2 in zip(
                    timestamps_210[:-1], timestamps_210[1:]
                )
            ]
            packets_211_time_diffs = [
                timestamp2 - timestamp1
                for timestamp1, timestamp2 in zip(
                    timestamps_211[:-1], timestamps_211[1:]
                )
            ]
            packets_212_time_diffs = [
                timestamp2 - timestamp1
                for timestamp1, timestamp2 in zip(
                    timestamps_212[:-1], timestamps_212[1:]
                )
            ]

            step.verify_equal(
                "Verify that for each of the CAN IDs the time between triple packets is 10ms ± 0.5ms apart",
                True,
                all([10 == time_diff for time_diff in packets_210_time_diffs]),
                f"Messages 0x210 received in time (ms): {timestamps_210}",
            )
            step.verify_equal(
                "Verify that for each of the CAN IDs the time between triple packets is 10ms ± 0.5ms apart",
                True,
                all([10 == time_diff for time_diff in packets_211_time_diffs]),
                f"Messages 0x211 received in time (ms): {timestamps_211}",
            )
            step.verify_equal(
                "Verify that for each of the CAN IDs the time between triple packets is 10ms ± 0.5ms apart",
                True,
                all([10 == time_diff for time_diff in packets_212_time_diffs]),
                f"Messages 0x212 received in time (ms): {timestamps_212}",
            )

        with report.TestStep(
            "Examine the auxiliary data type (Byte 3) in CAN message 0x211"
        ) as step:
            aux_data_messages: List[int] = []

            for _ in range(100):
                aux_data_type = foot_switch.wired_conn.get_status_211()
                assert (
                    aux_data_type is not None
                ), "Failed to receive StatusMsg211 message"
                aux_data_messages.append(aux_data_type.aux_type)

            aux_data_results = self.examine_auxiliary_data_type(aux_data_messages)

            step.verify_equal(
                "Verify that the auxiliary data type field is cycled from 0x0 to 0x1F",
                aux_data_results,
                True,
            )

    def test_disable_beacons(self, foot_switch: FootSwitch) -> None:
        """
        [FSW0122].
        """
        with report.TestStep("Cable Footswitch to CANoe") as step:
            foot_switch_state, message = connect_footswitch_to_console(foot_switch)

            step.verify_equal(
                "The “Connection” as “Cabled”.",
                FootSwitchState.Cabled,
                foot_switch_state,
                comment=f"Status message: {message}",
            )

        with report.TestStep(
            "Enable periodic transmission of CAN beacon_status (CAN ID 0x310 and CAN ID 0x311 every 80ms) using CANoe."
        ) as step:
            foot_switch.wired_conn.enable_beacons(0.08, beacons=BEACONS)
            step.verify_equal(
                "The Beacons are enabled",
                True,
                self.beacons_enabled(foot_switch),
            )

        with report.TestStep("Stop transmitting both CAN beacons from CANoe") as step:
            foot_switch.wired_conn.disable_beacons()
            step.verify_equal(
                "The Beacons are disabled",
                False,
                self.beacons_enabled(foot_switch),
            )

        with report.TestStep("Enable periodic transmission of CAN beacons") as step:
            foot_switch.wired_conn.enable_beacons(0.08, beacons=BEACONS)
            step.verify_equal(
                "The Beacons are enabled",
                True,
                self.beacons_enabled(foot_switch),
            )
