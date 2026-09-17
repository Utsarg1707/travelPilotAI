"""Pydantic schemas and TravelState package."""

from backend.app.schemas.budget import BudgetAnalysis, CostBreakdown
from backend.app.schemas.flights import FlightOption, FlightSearchResult
from backend.app.schemas.guardrails import (
    GuardrailResults,
    InputGuardrailResult,
    OutputGuardrailResult,
)
from backend.app.schemas.hotels import HotelOption, HotelSearchResult
from backend.app.schemas.itinerary import Attraction, Itinerary, ItineraryActivity, ItineraryDay
from backend.app.schemas.requests import NormalizedTravelRequest, TravelDates
from backend.app.schemas.supervisor import SupervisorDecision
from backend.app.schemas.travel_state import ToolCallInfo, TravelState
from backend.app.schemas.weather import WeatherForecastDay, WeatherResult

__all__ = [
    "Attraction",
    "BudgetAnalysis",
    "CostBreakdown",
    "FlightOption",
    "FlightSearchResult",
    "GuardrailResults",
    "HotelOption",
    "HotelSearchResult",
    "InputGuardrailResult",
    "Itinerary",
    "ItineraryActivity",
    "ItineraryDay",
    "NormalizedTravelRequest",
    "OutputGuardrailResult",
    "SupervisorDecision",
    "ToolCallInfo",
    "TravelDates",
    "TravelState",
    "WeatherForecastDay",
    "WeatherResult",
]
