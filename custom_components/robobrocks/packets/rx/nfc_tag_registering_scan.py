"""RX Packet: NFC Tag Registering Scan."""
from ...ble.const import RobobrocksHistoryEvent
from ...logic.anonymizer import RobobrocksAnonymizer
from ..base import RobobrocksHistoryLogPacket


class NfcTagRegisteringScanPacket(RobobrocksHistoryLogPacket):
    """Log entry for an NFC tag registration scan."""

    OPCODES = RobobrocksHistoryEvent.NFC_TAG_REGISTERING_SCAN

    def __init__(self, raw_data: bytearray):
        super().__init__(RobobrocksHistoryEvent.NFC_TAG_REGISTERING_SCAN, raw_data)
        # Payload: [Age(3)] [Type(1)] [UID_Len(1)] [UID(NB)]
        self.tag_type = self.log_payload[0] if len(self.log_payload) >= 1 else 0
        self.uid_len = self.log_payload[1] if len(self.log_payload) >= 2 else 0
        self.uid = self.log_payload[2:2+self.uid_len].hex().upper() if self.uid_len else ""

    @property
    def extra_data(self) -> dict:
        return {"tag_type": self.tag_type, "scan_uid": self.uid}

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        display_uid = RobobrocksAnonymizer.anonymize_uid(self.uid, anonymize)
        return {
            "payload": f"Type={self.tag_type}, UID={display_uid}, {self._get_base_log_payload()}",
            "raw": self.raw_data.hex(),
            "suffix": " (ANONYMIZED)" if anonymize else ""
        }
