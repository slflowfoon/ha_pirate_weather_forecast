"""Constants for the Pirate Weather Daily Forecast integration."""
from datetime import timedelta

DOMAIN = "pirate_weather_forecast"

# Configuration constants
CONF_API_KEY = "api_key"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"

# API
API_ENDPOINT = "https://api.pirateweather.net/forecast/{api_key}/{latitude},{longitude}"
ATTRIBUTION = "Data provided by Pirate Weather"

# Update interval
UPDATE_INTERVAL = timedelta(minutes=60)
