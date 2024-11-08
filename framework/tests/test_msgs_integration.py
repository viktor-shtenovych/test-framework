import struct

from framework.communications.uvcs_fluidics.subsystem_msgs import (  # type: ignore
    BssAlertType,
    CommErrorType,
    SystemState,
    BssMechanismBssAlertMsg,
    BssMechanismBssConfigureMsg,
    UInt32,
    Double,
    Boolean,
)


def test_bss_alert_type_values() -> None:
    """! Test BssAlertType values."""
    assert int(BssAlertType.Invalid) == 0
    assert int(BssAlertType.None_) == 1
    assert int(BssAlertType.BssNotCalibrated) == 2
    assert int(BssAlertType.BssBpsZeroOffsetReferenceNotSet) == 3
    assert int(BssAlertType.ExcessiveBpsOffset) == 4
    assert int(BssAlertType.BagIdGainNotSet) == 5


def test_bss_alert_type_members() -> None:
    """! Test BssAlertType members."""
    enum_members = [
        member for member in dir(BssAlertType) if not member.startswith("_")
    ]
    expected_members = [
        "Invalid",
        "None_",
        "BssNotCalibrated",
        "BssBpsZeroOffsetReferenceNotSet",
        "ExcessiveBpsOffset",
        "BagIdGainNotSet",
    ]
    for member in expected_members:
        assert member in enum_members


def test_bss_alert_type_conversion() -> None:
    """! Test BssAlertType conversion."""
    assert BssAlertType(0) == BssAlertType.Invalid
    assert BssAlertType(1) == BssAlertType.None_
    assert BssAlertType(2) == BssAlertType.BssNotCalibrated
    assert BssAlertType(3) == BssAlertType.BssBpsZeroOffsetReferenceNotSet
    assert BssAlertType(4) == BssAlertType.ExcessiveBpsOffset
    assert BssAlertType(5) == BssAlertType.BagIdGainNotSet


def test_bss_alert_type_string_representation() -> None:
    """! Test BssAlertType string representation."""
    assert str(BssAlertType.Invalid) == "Invalid"
    assert str(BssAlertType.None_) == "None"
    assert str(BssAlertType.BssNotCalibrated) == "BssNotCalibrated"
    assert (
        str(BssAlertType.BssBpsZeroOffsetReferenceNotSet)
        == "BssBpsZeroOffsetReferenceNotSet"
    )
    assert str(BssAlertType.ExcessiveBpsOffset) == "ExcessiveBpsOffset"
    assert str(BssAlertType.BagIdGainNotSet) == "BagIdGainNotSet"


def test_comm_error_type_values() -> None:
    """! Test CommErrorType enum values."""
    assert int(CommErrorType.Invalid) == 0
    assert int(CommErrorType.None_) == 1
    assert int(CommErrorType.CrcError) == 2
    assert int(CommErrorType.AckSequenceError) == 3
    assert int(CommErrorType.CommandSequenceError) == 4
    assert int(CommErrorType.UnexpectedMessage) == 5
    assert int(CommErrorType.ProtocolVersions) == 6
    assert int(CommErrorType.MissingAck) == 7


def test_comm_error_type_members() -> None:
    """! Test CommErrorType enum members."""
    enum_members = [
        member for member in dir(CommErrorType) if not member.startswith("_")
    ]
    expected_members = [
        "Invalid",
        "None_",
        "CrcError",
        "AckSequenceError",
        "CommandSequenceError",
        "UnexpectedMessage",
        "ProtocolVersions",
        "MissingAck",
    ]

    for member in expected_members:
        assert member in enum_members


def test_comm_error_type_conversion() -> None:
    """! Test integer to CommErrorType enum conversion."""
    assert CommErrorType(0) == CommErrorType.Invalid
    assert CommErrorType(1) == CommErrorType.None_
    assert CommErrorType(2) == CommErrorType.CrcError
    assert CommErrorType(3) == CommErrorType.AckSequenceError
    assert CommErrorType(4) == CommErrorType.CommandSequenceError
    assert CommErrorType(5) == CommErrorType.UnexpectedMessage
    assert CommErrorType(6) == CommErrorType.ProtocolVersions
    assert CommErrorType(7) == CommErrorType.MissingAck


def test_system_state_values() -> None:
    """! Test SystemState enum values."""
    assert int(SystemState.Invalid) == 0
    assert int(SystemState.Setup) == 1
    assert int(SystemState.Surgery) == 2
    assert int(SystemState.Service) == 3
    assert int(SystemState.Shutdown) == 4
    assert int(SystemState.Faulted) == 5


def test_system_state_members() -> None:
    """! Test SystemState enum members."""
    enum_members = [member for member in dir(SystemState) if not member.startswith("_")]
    expected_members = [
        "Invalid",
        "Setup",
        "Surgery",
        "Service",
        "Shutdown",
        "Faulted",
    ]
    for member in expected_members:
        assert member in enum_members


def test_system_state_conversion() -> None:
    """! Test integer to SystemState enum conversion."""
    assert SystemState(0) == SystemState.Invalid
    assert SystemState(1) == SystemState.Setup
    assert SystemState(2) == SystemState.Surgery
    assert SystemState(3) == SystemState.Service
    assert SystemState(4) == SystemState.Shutdown
    assert SystemState(5) == SystemState.Faulted


def test_bss_alert_msg_pack_unpack() -> None:
    """! Test BssMechanismBssAlertMsg pack and unpack."""
    bss_alert = BssAlertType.Invalid
    bss_alert_detail = UInt32(123)

    msg = BssMechanismBssAlertMsg(bss_alert, bss_alert_detail)
    frame_payload = struct.pack(">BB", bss_alert, bss_alert_detail)
    msg.EncodeMsgContent(frame_payload)
    msg_unpacked = BssMechanismBssAlertMsg(frame_payload)

    assert msg_unpacked.BssAlert == msg.BssAlert
    assert msg_unpacked.BssAlertDetail == msg.BssAlertDetail


def test_bss_configure_msg_pack_unpack() -> None:
    """! Test BssMechanismBssConfigureMsg pack and unpack."""
    bag_pressure_setpoint = Double(500.0)
    enable_post = Boolean(True)
    active_backup_mode = Boolean(False)
    active_backup_mode_setpoint = Double(250.0)
    dev_field1 = UInt32(42)

    msg = BssMechanismBssConfigureMsg(
        bag_pressure_setpoint,
        enable_post,
        active_backup_mode,
        active_backup_mode_setpoint,
        dev_field1,
    )
    # Scaling factors (as per C# code, scaling factor is 10)
    scaling_factor = 10

    # Convert doubles to scaled Int16
    bag_pressure_setpoint_int = int(bag_pressure_setpoint) * scaling_factor
    active_backup_mode_setpoint_int = int(
        float(active_backup_mode_setpoint) * scaling_factor
    )

    # Pack booleans into a single byte
    # Bits:
    # Bit 0: enable_post
    # Bit 1: active_backup_mode
    # Bits 2-7: unused (set to 0
    packed_booleans = (int(enable_post) << 0) | (int(active_backup_mode) << 1)

    struct_format = ">hB hI"
    frame_payload = struct.pack(
        struct_format,
        bag_pressure_setpoint_int,
        packed_booleans,
        active_backup_mode_setpoint_int,
        dev_field1,
    )
    msg.EncodeMsgContent(frame_payload)
    msg_unpacked = BssMechanismBssConfigureMsg(frame_payload)

    assert msg_unpacked.BagPressureSetpoint == msg.BagPressureSetpoint
    assert msg_unpacked.EnablePost == msg.EnablePost
    assert msg_unpacked.ActiveBackupMode == msg.ActiveBackupMode
    assert msg_unpacked.ActiveBackupModeSetpoint == msg.ActiveBackupModeSetpoint
    assert msg_unpacked.DevField1 == msg.DevField1
