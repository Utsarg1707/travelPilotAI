"""MCP Weather Server providing get_weather_forecast tool."""

from typing import Any, Dict
from backend.app.providers.weather_provider import FreeWeatherProvider

provider = FreeWeatherProvider()


def get_weather_forecast(destination: str, days: int = 5) -> Dict[str, Any]:
    """MCP Tool: Retrieve destination weather forecast."""
    res = provider.get_weather_forecast(destination=destination, days=days)
    return res.model_dump()
