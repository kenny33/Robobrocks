"""Registry of the permanent (master) codes stored in the Robobrocks slots.

The device can only report how many permanent codes it holds, never which ones.
This registry keeps the slot -> code mapping in Home Assistant so the codes are
never lost and can be written back to the device.

Storage is keyed by the Bluetooth address (not the config entry id), so the
registry survives removing and re-adding the integration for the same box.
"""
import logging
from datetime import datetime

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1
STORAGE_KEY_TEMPLATE = "robobrocks_permanent_codes_{}"


class RobobrocksPermanentCodeStore:
    """Slot registry for permanent codes."""

    def __init__(self, hass: HomeAssistant, address: str) -> None:
        self._store = Store(
            hass,
            STORAGE_VERSION,
            STORAGE_KEY_TEMPLATE.format(address.replace(":", "").lower()),
        )
        self._slots: dict[int, dict] = {}

    async def load(self) -> None:
        """Load the registry from storage."""
        data = await self._store.async_load() or {}
        self._slots = {int(index): slot for index, slot in data.get("slots", {}).items()}

    async def _save(self) -> None:
        await self._store.async_save({"slots": {str(i): s for i, s in self._slots.items()}})

    @property
    def slots(self) -> dict[int, dict]:
        """Return the slots, sorted by index."""
        return dict(sorted(self._slots.items()))

    def get(self, index: int) -> dict | None:
        """Return one slot."""
        return self._slots.get(index)

    def find_code(self, code: str) -> int | None:
        """Return the slot holding this code, if any."""
        code = (code or "").strip().upper()
        for index, slot in self._slots.items():
            if slot["code"] == code:
                return index
        return None

    def first_free(self, start: int = 1) -> int:
        """Return the first slot index not used in the registry."""
        index = start
        while index in self._slots:
            index += 1
        return index

    async def set_slot(self, index: int, code: str, label: str) -> None:
        """Create or replace a slot."""
        self._slots[index] = {
            "code": code.strip().upper(),
            "label": label.strip(),
            "added_at": datetime.now().isoformat(timespec="seconds"),
        }
        await self._save()

    async def set_label(self, index: int, label: str) -> None:
        """Rename a slot."""
        self._slots[index]["label"] = label.strip()
        await self._save()

    async def mark_used(self, index: int, timestamp: float) -> bool:
        """Record a use of the slot. Return False if this use was already recorded."""
        slot = self._slots[index]
        # Log times are rebuilt from the entry age at download time, so the same entry
        # read twice can differ by a second or two.
        if timestamp and timestamp <= slot.get("last_used_ts", 0) + 5:
            return False
        when = dt_util.as_local(dt_util.utc_from_timestamp(timestamp)) if timestamp else dt_util.now()
        slot["last_used_ts"] = timestamp or when.timestamp()
        slot["last_used"] = when.isoformat(timespec="seconds")
        await self._save()
        return True

    async def remove_slot(self, index: int) -> None:
        """Remove a slot."""
        self._slots.pop(index, None)
        await self._save()
