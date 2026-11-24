"""TX Packet: Delete Multi Use Code."""
from ...ble.const import RobobrocksCommandOpcode
from ...logic.anonymizer import RobobrocksAnonymizer
from ..base import RobobrocksTXPacket


class DeleteMultiUseCodePacket(RobobrocksTXPacket):
    """Command to delete a multi-use PIN code by its value."""

    def __init__(self, config_key: str, pin: str):
        super().__init__(RobobrocksCommandOpcode.DELETE_MULTI_USE_CODE)
        self.config_key = config_key
        self.pin = pin

    def to_bytes(self) -> bytearray:
        # Payload: ConfigKey (8) + PIN (6)
        payload = bytearray(self.config_key.encode('ascii'))
        payload.extend(self.pin.encode('ascii'))
        return self._build_framed_packet(payload)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        log_pin = RobobrocksAnonymizer.anonymize_pin(self.pin, anonymize)
        log_key = RobobrocksAnonymizer.anonymize_key(self.config_key, anonymize)
        return {
            "payload": f"Key={log_key}, PIN={log_pin}",
            "raw": self.to_bytes().hex(),
            "suffix": " (ANONYMIZED)" if anonymize else ""
        }
