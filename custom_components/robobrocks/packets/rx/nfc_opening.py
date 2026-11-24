"""RX Packet: NFC Opening."""
from ...ble.const import RobobrocksHistoryEvent
from ...logic.anonymizer import RobobrocksAnonymizer
from ..base import RobobrocksHistoryLogPacket


class NfcOpeningPacket(RobobrocksHistoryLogPacket):
    """Notification for an NFC opening."""

    OPCODES = RobobrocksHistoryEvent.NFC_OPENING

    def __init__(self, raw_data: bytearray):
        super().__init__(RobobrocksHistoryEvent.NFC_OPENING, raw_data)
        # log_payload starts after Age(3)
        self.tag_type = self.log_payload[0] if len(self.log_payload) >= 1 else 0
        self.uid_len = self.log_payload[1] if len(self.log_payload) >= 2 else 0
        self.uid = self.log_payload[2:2+self.uid_len].hex().upper() if self.uid_len else ""

    @property
    def extra_data(self) -> dict:
        return {"tag_type": self.tag_type, "tag_uid": self.uid}

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        display_uid = RobobrocksAnonymizer.anonymize_uid(self.uid, anonymize)
        return {
            "payload": f"Type={self.tag_type}, UID={display_uid}, {self._get_base_log_payload()}",
            "raw": self.raw_data.hex(),
            "suffix": " (ANONYMIZED)" if anonymize else ""
        }
