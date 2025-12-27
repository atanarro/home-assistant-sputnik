"""Sensor platform for Sputnik Climbing."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SputnikCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Sputnik Climbing sensors."""
    coordinator: SputnikCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for center_name in coordinator.data:
        entities.append(SputnikOccupancySensor(coordinator, center_name))
        entities.append(SputnikPercentageSensor(coordinator, center_name))

    async_add_entities(entities)


class SputnikOccupancySensor(CoordinatorEntity, SensorEntity):
    """Sensor showing current occupancy count."""

    def __init__(self, coordinator: SputnikCoordinator, center: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._center = center
        self._attr_name = f"Sputnik {center.title()} Occupancy"
        self._attr_unique_id = f"sputnik_{center.replace(' ', '_')}_occupancy"
        self._attr_icon = "mdi:account-group"
        self._attr_native_unit_of_measurement = "people"

    @property
    def native_value(self) -> int | None:
        """Return current occupancy."""
        if data := self.coordinator.data.get(self._center):
            return data["current"]
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional attributes."""
        if data := self.coordinator.data.get(self._center):
            return {"max_capacity": data["max"]}
        return {}


class SputnikPercentageSensor(CoordinatorEntity, SensorEntity):
    """Sensor showing occupancy percentage."""

    def __init__(self, coordinator: SputnikCoordinator, center: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._center = center
        self._attr_name = f"Sputnik {center.title()} Occupancy Percentage"
        self._attr_unique_id = f"sputnik_{center.replace(' ', '_')}_percentage"
        self._attr_icon = "mdi:percent"
        self._attr_native_unit_of_measurement = "%"

    @property
    def native_value(self) -> float | None:
        """Return occupancy percentage."""
        if data := self.coordinator.data.get(self._center):
            return data["percentage"]
        return None

