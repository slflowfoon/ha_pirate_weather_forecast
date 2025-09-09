"""DataUpdateCoordinator for the Pirate Weather Daily Forecast integration."""
import logging
from async_timeout import timeout

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, API_ENDPOINT, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class PirateWeatherForecastCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Pirate Weather data."""

    def __init__(self, hass, api_key: str, latitude: float, longitude: float):
        """Initialize the data coordinator."""
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.session = async_get_clientsession(hass)
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from Pirate Weather API."""
        url = API_ENDPOINT.format(api_key=self.api_key, latitude=self.latitude, longitude=self.longitude)
        # Use 'si' units for Metric (Celsius)
        params = { "units": "si" }
        
        try:
            async with timeout(20):
                response = await self.session.get(url, params=params)
                if response.status != 200:
                    raise UpdateFailed(f"Error communicating with API: {response.status}")
                
                data = await response.json()
                if not data or "daily" not in data or "data" not in data["daily"]:
                    raise UpdateFailed("Invalid data received from Pirate Weather API")
                
                return data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
