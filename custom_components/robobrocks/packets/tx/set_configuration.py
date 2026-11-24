"""TX Packet: Set Configuration."""
from ...ble.const import RobobrocksCommandOpcode, RobobrocksConfigType
from ...logic.anonymizer import RobobrocksAnonymizer
from ..base import RobobrocksTXPacket


class SetConfigurationPacket(RobobrocksTXPacket):
    """Command to modify device configuration."""

    def __init__(self, config_key: str, config_type: RobobrocksConfigType, value: bool):
        """Initialize with config key, type and boolean value."""
        super().__init__(RobobrocksCommandOpcode.SET_CONFIGURATION)
        self.config_key = config_key
        self.config_type = config_type
        self.value = value

    def to_bytes(self) -> bytearray:
        """Build payload: [ConfigKey(8)][Type(1)][Value(1)]."""
        payload = bytearray(self.config_key.encode('ascii'))
        payload.append(self.config_type)
        payload.append(1 if self.value else 0)
        return self._build_framed_packet(payload)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        """Log info with masked key."""
        log_key = RobobrocksAnonymizer.anonymize_key(self.config_key, anonymize)

        return {
            "payload": f"Key={log_key}, Type={self.config_type.name}, Value={self.value}",
            "raw": self.to_bytes().hex(),
            "suffix": " (ANONYMIZED)" if anonymize else ""
        }
