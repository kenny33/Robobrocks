"""RX Packet: Door Closed."""
from ...ble.const import RobobrocksHistoryEvent
from ..base import RobobrocksHistoryLogPacket


class DoorClosedPacket(RobobrocksHistoryLogPacket):
    """Log entry for door closed event."""

    OPCODES = RobobrocksHistoryEvent.DOOR_CLOSED

    def __init__(self, raw_data: bytearray):
        super().__init__(RobobrocksHistoryEvent.DOOR_CLOSED, raw_data)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        return {
            "payload": self._get_base_log_payload(),
            "raw": self.raw_data.hex(),
            "suffix": ""
        }
