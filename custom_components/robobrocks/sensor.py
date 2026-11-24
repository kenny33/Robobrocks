"""Sensor platform for Robobrocks."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .sensors.battery import RobobrocksBatterySensor
from .sensors.battery_temperature import RobobrocksBatteryTemperatureSensor
from .sensors.codes import RobobrocksCodeCountSensor
from .sensors.diagnostics import (
    RobobrocksBatteryDiagnosticSensor,
    RobobrocksBatteryFormatSensor,
    RobobrocksBatteryTypeSensor,
)
from .sensors.last_event import RobobrocksLastEventSensor
from .sensors.log_count import RobobrocksLogCountSensor
from .sensors.maintenance import RobobrocksMaintenanceSensor


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Robobrocks sensors."""
    from homeassistant.components.sensor import SensorEntity
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = [
        RobobrocksBatterySensor(coordinator, entry),
        RobobrocksBatteryTemperatureSensor(coordinator, entry),
        RobobrocksLastEventSensor(coordinator, entry),
        RobobrocksBatteryFormatSensor(coordinator, entry),
        RobobrocksBatteryTypeSensor(coordinator, entry),
        RobobrocksMaintenanceSensor(coordinator, entry),
        RobobrocksLogCountSensor(coordinator, entry),
    ]

    # Add code count sensors
    from .ble.const import RobobrocksCodeType
    for code_type in [RobobrocksCodeType.MASTER, RobobrocksCodeType.SINGLE_USE]:
        entities.append(RobobrocksCodeCountSensor(coordinator, entry, code_type))

    # Check for battery format in config entry (persistent) or coordinator data (live)
    # This ensures sensors are created at boot if format was previously detected
    battery_format = entry.data.get("battery_format")

    if not battery_format:
        battery_stats = coordinator.data.get("battery_stats", {})
        battery_format = battery_stats.get("format")

    if battery_format == "measures-first-min-mean-max-last":
        entities.extend([
            RobobrocksBatteryDiagnosticSensor(coordinator, entry, "level_first"),
            RobobrocksBatteryDiagnosticSensor(coordinator, entry, "level_min"),
            RobobrocksBatteryDiagnosticSensor(coordinator, entry, "level_mean"),
            RobobrocksBatteryDiagnosticSensor(coordinator, entry, "level_max"),
            RobobrocksBatteryDiagnosticSensor(coordinator, entry, "level_last"),
        ])
    elif battery_format == "measures-t1-t5-t10":
        entities.extend([
            RobobrocksBatteryDiagnosticSensor(coordinator, entry, "level_t1"),
            RobobrocksBatteryDiagnosticSensor(coordinator, entry, "level_t5"),
            RobobrocksBatteryDiagnosticSensor(coordinator, entry, "level_t10"),
        ])

    # If "measure-single" or unknown, we don't add extra diagnostic sensors,
    # as the main RobobrocksBatterySensor covers the single level.
    async_add_entities(entities)
