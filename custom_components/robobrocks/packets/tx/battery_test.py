"""TX Packet: Test Battery."""
from ...ble.const import RobobrocksCommandOpcode
from ..base import RobobrocksTXPacket


class BatteryTestPacket(RobobrocksTXPacket):
    """Command to trigger a battery test."""

    def __init__(self):
        super().__init__(RobobrocksCommandOpcode.TEST_BATTERY)

    def to_bytes(self) -> bytearray:
        return self._build_framed_packet(b"")
