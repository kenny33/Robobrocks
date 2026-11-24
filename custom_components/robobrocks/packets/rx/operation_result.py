"""RX Packet: Operation Result."""
from ...ble.const import RobobrocksNotificationOpcode
from ..base import RobobrocksRXPacket


class OperationResultPacket(RobobrocksRXPacket):
    """Notification for the success or failure of an operation."""

    OPCODES = [RobobrocksNotificationOpcode.CODE_OPERATION_SUCCESS, RobobrocksNotificationOpcode.CODE_OPERATION_ERROR]

    def __init__(self, opcode: int, raw_data: bytearray):
        """Initialize."""
        super().__init__(opcode, raw_data)
        self.success = (self.opcode == RobobrocksNotificationOpcode.CODE_OPERATION_SUCCESS)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        """Log info for operation result."""
        result = "SUCCESS" if self.success else "ERROR"
        return {
            "payload": f"Result={result}",
            "raw": self.raw_data.hex(),
            "suffix": ""
        }
