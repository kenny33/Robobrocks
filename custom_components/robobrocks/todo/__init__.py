import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import CONF_CONFIG_KEY, DOMAIN
from ..coordinator import RobobrocksDataUpdateCoordinator
from .entity import RobobrocksParcelTodoList
from .storage import RobobrocksParcelStore

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Robobrocks todo list."""
    coordinator: RobobrocksDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Initialize the store
    store = RobobrocksParcelStore(hass, entry.entry_id)
    await store.load()

    # Check if config key is present for BLE sync operations
    has_config_key = bool(entry.data.get(CONF_CONFIG_KEY))
    if not has_config_key:
        _LOGGER.info("Robobrocks Config Key missing: Parcel Todo List will run in tracking-only mode (no code sync to Robobrocks).")

    entity = RobobrocksParcelTodoList(coordinator, entry, store, has_config_key)
    async_add_entities([entity])
