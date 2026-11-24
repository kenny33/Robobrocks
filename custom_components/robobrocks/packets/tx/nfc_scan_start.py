"""TX Packet: NFC Scan Start."""
from ...ble.const import RobobrocksCommandOpcode
from ...logic.anonymizer import RobobrocksAnonymizer
from ..base import RobobrocksTXPacket


class NfcScanStartPacket(RobobrocksTXPacket):
    """Command to start NFC tag scanning mode."""

    def __init__(self, config_key: str):
        super().__init__(RobobrocksCommandOpcode.REGISTER_NFC_TAG_SCAN_START)
        self.config_key = config_key

    def to_bytes(self) -> bytearray:
        # Payload: ConfigKey (8)
        payload = self.config_key.encode('ascii')
        return self._build_framed_packet(payload)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        log_key = RobobrocksAnonymizer.anonymize_key(self.config_key, anonymize)
        return {
            "payload": f"Key={log_key}",
            "raw": self.to_bytes().hex(),
            "suffix": " (ANONYMIZED)" if anonymize else ""
        }
