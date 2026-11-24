"""TX Packet: Reboot."""
from ...ble.const import RobobrocksCommandOpcode
from ..base import RobobrocksTXPacket


class RebootPacket(RobobrocksTXPacket):
    """Command to trigger a software reboot."""

    def __init__(self):
        super().__init__(RobobrocksCommandOpcode.REBOOT)

    def to_bytes(self) -> bytearray:
        return self._build_framed_packet(b"")
