from enum import IntEnum
import bitstruct
import dataclasses


class ScanResult(IntEnum):
    """
    Barcode Scan Result Type.
    """

    UnexpectedCommand = 1
    BarcodeNotDetected = 2
    BarcodeDetected = 3
    BarcodeDecoded = 4
    BarcodeInvalidCRC = 5


@dataclasses.dataclass
class BarcodeReaderScanReply:
    """
    Barcode Reader Scan Reply.
    """

    scan_result: ScanResult
    scan_count: int
    bc_upper_left_x: int
    bc_upper_left_y: int
    bc_width: int
    bc_height: int
    bc_quality_grade: int
    bc_contrast: int
    bc_unused_error_correction: int
    bc_decode_data: str

    @classmethod
    def unpack(cls, data: bytes) -> "BarcodeReaderScanReply":
        """
        Unpack data.

        Args:
            data: Data to unpack.

        Returns:
            BarcodeReaderScanReply: Unpacked data.
        """
        (
            scan_result,
            scan_count,
            bc_upper_left_x,
            bc_upper_left_y,
            bc_width,
            bc_height,
            bc_quality_grade,
            bc_contrast,
            bc_unused_error_correction,
            bc_decode_data,
        ) = tuple(bitstruct.unpack("u8u8u16u16u16u16u8u8u8t30", data))
        return BarcodeReaderScanReply(
            scan_result=ScanResult(scan_result),
            scan_count=scan_count,
            bc_upper_left_x=bc_upper_left_x,
            bc_upper_left_y=bc_upper_left_y,
            bc_width=bc_width,
            bc_height=bc_height,
            bc_quality_grade=bc_quality_grade,
            bc_contrast=bc_contrast,
            bc_unused_error_correction=bc_unused_error_correction,
            bc_decode_data=bc_decode_data,
        )
