"""RX Packet: Key Opening."""
from ...ble.const import RobobrocksHistoryEvent
from ..base import RobobrocksHistoryLogPacket


class KeyOpeningPacket(RobobrocksHistoryLogPacket):
    """Log entry for key opening event."""

    OPCODES = RobobrocksHistoryEvent.KEY_OPENING

    def __init__(self, raw_data: bytearray):
        super().__init__(RobobrocksHistoryEvent.KEY_OPENING, raw_data)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        return {
            "payload": self._get_base_log_payload(),
            "raw": self.raw_data.hex(),
            "suffix": ""
        }
