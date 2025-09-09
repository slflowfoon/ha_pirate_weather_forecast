"""The Pirate Weather Daily Forecast integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE, Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import PirateWeatherForecastCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pirate Weather Daily Forecast from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    api_key = entry.data[CONF_API_KEY]
    latitude = entry.data[CONF_LATITUDE]
    longitude = entry.data[CONF_LONGITUDE]

    coordinator = PirateWeatherForecastCoordinator(hass, api_key, latitude, longitude)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
