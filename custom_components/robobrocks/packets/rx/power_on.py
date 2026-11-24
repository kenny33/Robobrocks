"""RX Packet: Power On."""
from ...ble.const import RobobrocksHistoryEvent
from ..base import RobobrocksHistoryLogPacket


class PowerOnPacket(RobobrocksHistoryLogPacket):
    """Log entry for power on event."""

    OPCODES = RobobrocksHistoryEvent.POWER_ON

    def __init__(self, raw_data: bytearray):
        super().__init__(RobobrocksHistoryEvent.POWER_ON, raw_data)

    def to_log_dict(self, anonymize: bool = True) -> dict[str, str]:
        return {
            "payload": self._get_base_log_payload(),
            "raw": self.raw_data.hex(),
            "suffix": ""
        }
