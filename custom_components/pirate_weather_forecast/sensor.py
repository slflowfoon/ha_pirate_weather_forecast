"""Platform for Pirate Weather Daily Forecast sensor entities."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ATTRIBUTION
from .coordinator import PirateWeatherForecastCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: PirateWeatherForecastCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    # The API provides 8 days of forecasts
    for day_index in range(8):
        entities.append(PirateWeatherSummarySensor(coordinator, entry, day_index))
        entities.append(PirateWeatherApparentTempHighSensor(coordinator, entry, day_index))
    
    async_add_entities(entities)


class PirateWeatherForecastBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for Pirate Weather Forecast sensors."""

    def __init__(self, coordinator: PirateWeatherForecastCoordinator, entry: ConfigEntry, day_index: int):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._day_index = day_index
        self._attr_attribution = ATTRIBUTION

    @property
    def device_info(self):
        """Return device information."""
        unique_id = f"{self._entry.data[CONF_LATITUDE]}-{self._entry.data[CONF_LONGITUDE]}"
        return {
            "identifiers": {(DOMAIN, unique_id)},
            "name": f"Pirate Weather Forecast",
            "manufacturer": "Pirate Weather",
            "entry_type": "service",
        }
    
    @property
    def day_forecast(self):
        """Return the forecast data for the specific day from the coordinator."""
        try:
            return self.coordinator.data["daily"]["data"][self._day_index]
        except (KeyError, IndexError, TypeError):
            return None

    @property
    def _day_name(self) -> str:
        """Return a friendly name for the day index."""
        return f"Day {self._day_index}"


class PirateWeatherSummarySensor(PirateWeatherForecastBaseSensor):
    """Representation of the Daily Summary sensor."""

    _attr_icon = "mdi:text-long"
    
    def __init__(self, coordinator: PirateWeatherForecastCoordinator, entry: ConfigEntry, day_index: int):
        """Initialize the sensor."""
        super().__init__(coordinator, entry, day_index)
        unique_id = f"{entry.unique_id}_summary_day_{self._day_index}"
        self._attr_name = f"Pirate Weather Summary {self._day_name}"
        self._attr_unique_id = unique_id

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.day_forecast:
            return self.day_forecast.get("summary")
        return None


class PirateWeatherApparentTempHighSensor(PirateWeatherForecastBaseSensor):
    """Representation of the Apparent High Temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: PirateWeatherForecastCoordinator, entry: ConfigEntry, day_index: int):
        """Initialize the sensor."""
        super().__init__(coordinator, entry, day_index)
        unique_id = f"{entry.unique_id}_apparent_temp_high_day_{self._day_index}"
        self._attr_name = f"Pirate Weather Apparent Temp High {self._day_name}"
        self._attr_unique_id = unique_id

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.day_forecast:
            return self.day_forecast.get("apparentTemperatureHigh")
        return None
