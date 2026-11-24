"""TX Packet: Request Logs."""
from ...ble.const import RobobrocksCommandOpcode
from ..base import RobobrocksTXPacket


class RequestLogsPacket(RobobrocksTXPacket):
    """Simple command to request the log history."""

    def __init__(self):
        """Initialize."""
        super().__init__(RobobrocksCommandOpcode.REQUEST_LOGS)

    def to_bytes(self) -> bytearray:
        return self._build_framed_packet(b"")
