"""Weather Forecast Schemas."""

from pydantic import BaseModel, Field


class WeatherForecastDay(BaseModel):
    """Weather forecast for a single day."""

    date: str = Field(..., description="Forecast date (YYYY-MM-DD)")
    temp_max_c: float = Field(..., description="Maximum temperature in Celsius")
    temp_min_c: float = Field(..., description="Minimum temperature in Celsius")
    precipitation_prob: int = Field(0, ge=0, le=100, description="Precipitation probability %")
    weather_condition: str = Field(..., description="Weather description (e.g. 'Sunny', 'Rainy')")
    icon_code: str = Field("clear-day", description="Icon key for weather visualizer")


class WeatherResult(BaseModel):
    """Destination weather summary from Weather Agent."""

    destination: str = Field(..., description="Destination location")
    current_temp_c: float = Field(..., description="Current average temperature in Celsius")
    weather_summary: str = Field(..., description="Text summary of weather forecast")
    forecast: list[WeatherForecastDay] = Field(
        default_factory=list, description="Day-by-day forecast"
    )
    recommendations: list[str] = Field(
        default_factory=list, description="Weather-based travel recommendations"
    )
