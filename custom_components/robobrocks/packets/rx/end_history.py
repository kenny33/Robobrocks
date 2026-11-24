"""RX Packet: End History."""
from ...ble.const import RobobrocksHistoryEvent
from ..base import RobobrocksHistoryLogPacket


class EndHistoryPacket(RobobrocksHistoryLogPacket):
    """Log entry for end of history event."""

    OPCODES = RobobrocksHistoryEvent.LOG_END_HISTORY

    def __init__(self, raw_data: bytearray):
        super().__init__(RobobrocksHistoryEvent.LOG_END_HISTORY, raw_data)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        return {
            "payload": self._get_base_log_payload(),
            "raw": self.raw_data.hex(),
            "suffix": ""
        }
