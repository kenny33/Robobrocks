"""TX Packet: Create Master Code."""
from ...ble.const import RobobrocksCommandOpcode
from ...logic.anonymizer import RobobrocksAnonymizer
from ..base import RobobrocksTXPacket


class CreateMasterCodePacket(RobobrocksTXPacket):
    """Command to create a permanent master code at a specific index."""

    def __init__(self, config_key: str, pin: str, index: int):
        super().__init__(RobobrocksCommandOpcode.CREATE_MASTER_CODE)
        self.config_key = config_key
        self.pin = pin
        self.index = index

    def to_bytes(self) -> bytearray:
        # Payload: ConfigKey (8) + PIN (6) + Index (1)
        payload = bytearray(self.config_key.encode('ascii'))
        payload.extend(self.pin.encode('ascii'))
        payload.append(self.index)
        return self._build_framed_packet(payload)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        log_pin = RobobrocksAnonymizer.anonymize_pin(self.pin, anonymize)
        log_key = RobobrocksAnonymizer.anonymize_key(self.config_key, anonymize)

        return {
            "payload": f"Key={log_key}, Index={self.index}, PIN={log_pin}",
            "raw": self.to_bytes().hex(),
            "suffix": " (ANONYMIZED)" if anonymize else ""
        }
