"""RX Packet: Door Opened."""
from ...ble.const import RobobrocksHistoryEvent
from ..base import RobobrocksHistoryLogPacket


class DoorOpenedPacket(RobobrocksHistoryLogPacket):
    """Log entry for door opened event."""

    OPCODES = RobobrocksHistoryEvent.DOOR_OPENED

    def __init__(self, raw_data: bytearray):
        super().__init__(RobobrocksHistoryEvent.DOOR_OPENED, raw_data)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        return {
            "payload": self._get_base_log_payload(),
            "raw": self.raw_data.hex(),
            "suffix": ""
        }
