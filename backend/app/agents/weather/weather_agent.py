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
        decision = state.get("supervisor_decision")
        destinations = state.get("destinations") or (
            decision.destinations if decision and decision.destinations else []
        )
        destination = state.get("destination") or (decision.destination if decision else "Dubai")
        duration = decision.duration_days if decision else 5

        if destinations and len(destinations) > 1:
            all_forecasts = []
            summaries = []
            recs = []
            provider = FreeWeatherProvider()
            days_per_city = max(3, duration // len(destinations))
            for city in destinations:
                res = provider.get_weather_forecast(destination=city, days=days_per_city)
                summaries.append(f"[{city}] {res.weather_summary}")
                all_forecasts.extend(res.forecast)
                if res.recommendations:
                    recs.extend(res.recommendations)

            unique_recs = list(dict.fromkeys(recs))
            result = WeatherResult(
                destination=destination,
                current_temp_c=all_forecasts[0].temp_max_c if all_forecasts else 28.5,
                weather_summary=" | ".join(summaries),
                forecast=all_forecasts,
                recommendations=unique_recs,
            )
        else:
            result = cls.get_forecast(destination=destination, days=duration)

        return {"weather_results": result}
