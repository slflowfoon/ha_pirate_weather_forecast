"""Config flow for Pirate Weather Daily Forecast integration."""
import voluptuous as vol
from typing import Any

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, API_ENDPOINT

class PirateWeatherForecastConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pirate Weather Daily Forecast."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> dict[str, Any]:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            session = async_get_clientsession(self.hass)
            api_key = user_input[CONF_API_KEY]
            latitude = user_input[CONF_LATITUDE]
            longitude = user_input[CONF_LONGITUDE]
            
            url = API_ENDPOINT.format(api_key=api_key, latitude=latitude, longitude=longitude)
            
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        unique_id = f"{latitude}-{longitude}"
                        await self.async_set_unique_id(unique_id)
                        self._abort_if_unique_id_configured()

                        return self.async_create_entry(
                            title=f"Pirate Weather {latitude}, {longitude}", data=user_input
                        )
                    if response.status in [401, 403]:
                        errors["base"] = "invalid_auth"
                    else:
                        errors["base"] = "cannot_connect"

            except Exception:
                errors["base"] = "cannot_connect"

        # Show the form to the user, pre-filling lat/long from HA config
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): cv.string,
                    vol.Required(CONF_LATITUDE, default=self.hass.config.latitude): cv.latitude,
                    vol.Required(CONF_LONGITUDE, default=self.hass.config.longitude): cv.longitude,
                }
            ),
            errors=errors,
        )
