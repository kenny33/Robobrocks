"""RX Packet: Error Response."""
from ...ble.const import RobobrocksNotificationOpcode
from ..base import RobobrocksRXPacket


class ErrorResponsePacket(RobobrocksRXPacket):
    """Generic representation of an error notification (CRC, Auth, etc.)."""

    OPCODES = [
        RobobrocksNotificationOpcode.ERROR_CRC,
        RobobrocksNotificationOpcode.ERROR_UNAUTHORIZED,
        RobobrocksNotificationOpcode.ERROR_BAD_REQUEST
    ]

    def __init__(self, opcode: int, raw_data: bytearray):
        """Initialize."""
        super().__init__(opcode, raw_data)

    @property
    def error_type(self) -> str:
        """Return a string identifying the error type."""
        if self.opcode == RobobrocksNotificationOpcode.ERROR_CRC:
            return "CRC_ERROR"
        if self.opcode == RobobrocksNotificationOpcode.ERROR_UNAUTHORIZED:
            return "AUTH_ERROR"
        if self.opcode == RobobrocksNotificationOpcode.ERROR_BAD_REQUEST:
            return "BAD_REQUEST"
        return "UNKNOWN_ERROR"

    @property
    def extra_data(self) -> dict:
        return {"error_type": self.error_type}

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        """Log info for error."""
        return {
            "payload": f"Error={self.error_type}",
            "raw": self.raw_data.hex(),
            "suffix": ""
        }
