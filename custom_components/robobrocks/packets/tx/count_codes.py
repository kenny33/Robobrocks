"""TX Packet: Count Codes."""
from ...ble.const import RobobrocksCommandOpcode
from ..base import RobobrocksTXPacket


class CountCodesPacket(RobobrocksTXPacket):
    """Simple command to request the current code counts."""

    def __init__(self):
        """Initialize."""
        super().__init__(RobobrocksCommandOpcode.COUNT_CODES)

    def to_bytes(self) -> bytearray:
        return self._build_framed_packet(b"")
