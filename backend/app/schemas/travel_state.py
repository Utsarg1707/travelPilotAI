"""Shared Typed State Definition for LangGraph Workflow."""

import operator
from typing import Annotated, Any, TypedDict

from pydantic import BaseModel, Field

from backend.app.schemas.budget import BudgetAnalysis
from backend.app.schemas.flights import FlightSearchResult
from backend.app.schemas.guardrails import InputGuardrailResult, OutputGuardrailResult
from backend.app.schemas.hotels import HotelSearchResult
from backend.app.schemas.itinerary import Attraction, Itinerary
from backend.app.schemas.requests import NormalizedTravelRequest, TravelDates
from backend.app.schemas.supervisor import SupervisorDecision
from backend.app.schemas.weather import WeatherResult


def max_int_reducer(current: int, incoming: int) -> int:
    """Reducer function to combine integer iteration counts in concurrent nodes."""
    return max(current or 0, incoming or 0)


class ToolCallInfo(BaseModel):
    """Execution metadata for tools called during workflow."""

    agent_name: str = Field(..., description="Name of calling agent")
    tool_name: str = Field(..., description="Name of executed MCP/local tool")
    arguments: dict[str, Any] = Field(default_factory=dict, description="Tool invocation parameters")
    result_summary: str = Field(..., description="Summary of tool output")
    execution_time_ms: float = Field(0.0, ge=0.0, description="Latency in milliseconds")
    is_demo: bool = Field(True, description="Demo provider flag")
    timestamp: str = Field(..., description="ISO 8601 execution timestamp")


class TravelState(TypedDict, total=False):
    """Shared typed state dict passed between all LangGraph nodes."""

    session_id: str
    request_id: str
    user_query: str
    normalized_request: NormalizedTravelRequest | None
    origin: str | None
    destination: str | None
    travel_dates: TravelDates | None
    travelers: int | None
    preferences: list[str]
    budget: float | None

    selected_agents: list[str]
    supervisor_decision: SupervisorDecision | None

    flight_results: FlightSearchResult | None
    hotel_results: HotelSearchResult | None
    weather_results: WeatherResult | None
    attractions: list[Attraction] | None
    budget_analysis: BudgetAnalysis | None
    itinerary: Itinerary | None

    input_guardrail: InputGuardrailResult | None
    output_guardrail: OutputGuardrailResult | None

    tool_calls: Annotated[list[ToolCallInfo], operator.add]
    errors: Annotated[list[str], operator.add]
    warnings: Annotated[list[str], operator.add]

    approval_status: str | None  # 'pending', 'approved', 'rejected', 'edited'
    human_feedback: str | None
    final_response: str | None

    graph_iteration_count: Annotated[int, max_int_reducer]
    is_completed: bool
