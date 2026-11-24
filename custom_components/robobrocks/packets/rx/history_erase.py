"""RX Packet: History Erase."""
from ...ble.const import RobobrocksHistoryEvent
from ..base import RobobrocksHistoryLogPacket


class HistoryErasePacket(RobobrocksHistoryLogPacket):
    """Log entry for history erase event."""

    OPCODES = RobobrocksHistoryEvent.HISTORY_ERASE

    def __init__(self, raw_data: bytearray):
        super().__init__(RobobrocksHistoryEvent.HISTORY_ERASE, raw_data)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        return {
            "payload": self._get_base_log_payload(),
            "raw": self.raw_data.hex(),
            "suffix": ""
        }
