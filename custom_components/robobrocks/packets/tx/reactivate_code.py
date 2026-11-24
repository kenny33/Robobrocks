"""TX Packet: Reactivate Code."""
from ...ble.const import RobobrocksCommandOpcode
from ...logic.anonymizer import RobobrocksAnonymizer
from ..base import RobobrocksTXPacket


class ReactivateCodePacket(RobobrocksTXPacket):
    """Command to reactivate a previously deactivated PIN code."""

    def __init__(self, config_key: str, code_value: str):
        super().__init__(RobobrocksCommandOpcode.REACTIVATE_CODE)
        self.config_key = config_key
        self.code_value = code_value

    def to_bytes(self) -> bytearray:
        # Payload: [ConfigKey(8)][CodeValue(NB)]
        payload = bytearray(self.config_key.encode('ascii'))
        payload.extend(self.code_value.encode('ascii'))
        return self._build_framed_packet(payload)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        log_key = RobobrocksAnonymizer.anonymize_key(self.config_key, anonymize)
        log_code = RobobrocksAnonymizer.anonymize_pin(self.code_value, anonymize)
        return {
            "payload": f"Key={log_key}, Code={log_code}",
            "raw": self.to_bytes().hex(),
            "suffix": " (ANONYMIZED)" if anonymize else ""
        }
