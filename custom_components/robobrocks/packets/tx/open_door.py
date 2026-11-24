"""TX Packet: Open Door."""
from ...ble.const import RobobrocksCommandOpcode
from ...logic.anonymizer import RobobrocksAnonymizer
from ..base import RobobrocksTXPacket


class OpenDoorPacket(RobobrocksTXPacket):
    """Command to open the door with a required PIN."""

    def __init__(self, pin: str):
        if not pin:
            raise ValueError("PIN is required for Open Door command")
        super().__init__(RobobrocksCommandOpcode.OPEN_DOOR)
        self.pin = pin

    def to_bytes(self) -> bytearray:
        payload = self.pin.encode('ascii')
        return self._build_framed_packet(payload)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        log_pin = RobobrocksAnonymizer.anonymize_pin(self.pin, anonymize)
        raw_bytes = self.to_bytes()

        return {
            "payload": log_pin or "",
            "raw": raw_bytes.hex(),
            "suffix": " (ANONYMIZED)" if anonymize and self.pin else ""
        }
