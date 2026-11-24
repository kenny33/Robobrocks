"""TX Packet: Ask Door Status."""
from ...ble.const import RobobrocksCommandOpcode
from ..base import RobobrocksTXPacket


class AskDoorStatusPacket(RobobrocksTXPacket):
    """Simple command to request the current door status."""

    def __init__(self):
        """Initialize."""
        super().__init__(RobobrocksCommandOpcode.ASK_DOOR_STATUS)

    def to_bytes(self) -> bytearray:
        return self._build_framed_packet(b"")
