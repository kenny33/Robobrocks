"""Battery format sensor for Robobrocks."""
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS, EntityCategory

from ...coordinator import RobobrocksDataUpdateCoordinator
from .retaining_sensor import RobobrocksRetainingSensor


class RobobrocksBatteryFormatSensor(RobobrocksRetainingSensor):
    """Representation of a Robobrocks Battery Format Sensor (Measurement Format)."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["unknown", "measures-first-min-mean-max-last", "measures-t1-t5-t10", "measure-single", "other"]
    _attr_icon = "mdi:battery-heart"

    def __init__(self, coordinator: RobobrocksDataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_translation_key = "battery_format"
        self._attr_unique_id = f"{entry.data[CONF_ADDRESS]}_battery_format"

    def _get_current_value(self) -> str | None:
        """Return the current battery measurement format from coordinator."""
        stats = self.coordinator.data.get("battery_stats")
        if stats:
            raw = stats.get("format")
            if raw:
                return raw
        return "unknown"

    @property
    def suggested_object_id(self) -> str | None:
        """Return the suggested object id."""
        return "battery_format"
