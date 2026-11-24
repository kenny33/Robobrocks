"""TX Packet: Get Logs Count."""
from ...ble.const import RobobrocksCommandOpcode
from ..base import RobobrocksTXPacket


class GetLogsCountPacket(RobobrocksTXPacket):
    """Simple command to request the number of available logs."""

    def __init__(self):
        """Initialize."""
        super().__init__(RobobrocksCommandOpcode.GET_LOGS_COUNT)

    def to_bytes(self) -> bytearray:
        return self._build_framed_packet(b"")
