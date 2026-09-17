"""Flight, Hotel, Weather provider adapters package."""

from backend.app.providers.flight_provider import DemoFlightProvider, FlightProvider
from backend.app.providers.hotel_provider import DemoHotelProvider, HotelProvider
from backend.app.providers.weather_provider import FreeWeatherProvider, WeatherProvider

__all__ = [
    "DemoFlightProvider",
    "DemoHotelProvider",
    "FlightProvider",
    "FreeWeatherProvider",
    "HotelProvider",
    "WeatherProvider",
]
