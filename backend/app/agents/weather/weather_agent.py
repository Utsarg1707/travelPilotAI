"""Weather Specialist Agent using Free Weather Provider."""


from backend.app.providers.weather_provider import FreeWeatherProvider
from backend.app.schemas.travel_state import TravelState
from backend.app.schemas.weather import WeatherResult


class WeatherAgent:
    """Specialist Agent responsible for destination weather forecasts."""

    @classmethod
    def get_forecast(cls, destination: str = "Dubai", days: int = 5) -> WeatherResult:
        """Fetch weather forecast via free Open-Meteo API (with fallback)."""
        provider = FreeWeatherProvider()
        return provider.get_weather_forecast(destination=destination, days=days)

    @classmethod
    def run_node(cls, state: TravelState) -> TravelState:
        """Execute Weather Agent as a LangGraph node handler."""
        destination = state.get("destination") or "Dubai"
        duration = state.get("supervisor_decision").duration_days if state.get("supervisor_decision") else 5

        result = cls.get_forecast(destination=destination, days=duration)
        return {"weather_results": result}
