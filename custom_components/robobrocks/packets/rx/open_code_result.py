"""RX Packet: Open Code Validation Result."""
from ...ble.const import RobobrocksNotificationOpcode
from ..base import RobobrocksRXPacket


class OpenCodeResultPacket(RobobrocksRXPacket):
    """Notification confirming if an opening code was valid or not."""

    OPCODES = [RobobrocksNotificationOpcode.VALID_OPEN_CODE, RobobrocksNotificationOpcode.INVALID_OPEN_CODE]

    def __init__(self, opcode: int, raw_data: bytearray):
        super().__init__(opcode, raw_data)
        self.valid = (self.opcode == RobobrocksNotificationOpcode.VALID_OPEN_CODE)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        """Log info for code validation result."""
        result = "VALID" if self.valid else "INVALID"
        return {
            "payload": f"Result={result}",
            "raw": self.raw_data.hex(),
            "suffix": ""
        }
