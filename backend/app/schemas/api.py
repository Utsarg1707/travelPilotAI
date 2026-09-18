"""API Request and Response Models."""

from typing import Any

from pydantic import BaseModel, Field

from backend.app.schemas.budget import BudgetAnalysis
from backend.app.schemas.flights import FlightSearchResult
from backend.app.schemas.hotels import HotelSearchResult
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.supervisor import SupervisorDecision
from backend.app.schemas.travel_state import ToolCallInfo
from backend.app.schemas.weather import WeatherResult


class PlanRequest(BaseModel):
    """Request payload for initiating a travel plan workflow."""

    user_query: str = Field(
        ...,
        json_schema_extra={
            "example": "Plan a 5-day trip to Dubai from Bangalore for 2 people with a budget of ₹1,50,000."
        },
    )
    session_id: str | None = Field(
        None, description="Optional existing session ID for context continuation"
    )


class PlanResponse(BaseModel):
    """Response payload returned from travel plan workflow endpoint."""

    session_id: str = Field(..., description="Unique session identifier")
    request_id: str = Field(..., description="Unique request tracking identifier")
    status: str = Field(
        ..., description="Execution status: 'completed', 'waiting_for_approval', 'blocked', 'error'"
    )
    approval_status: str = Field(
        "pending", description="Approval state: 'pending', 'approved', 'edited', 'rejected'"
    )
    supervisor_decision: SupervisorDecision | None = Field(
        None, description="Supervisor routing metadata"
    )
    selected_agents: list[str] = Field(
        default_factory=list, description="Specialist agents invoked"
    )
    final_response: str | None = Field(None, description="Synthesized user-facing response text")
    tool_calls: list[ToolCallInfo] = Field(
        default_factory=list, description="Executed tool metadata"
    )
    flight_results: FlightSearchResult | None = Field(None, description="Flight search options")
    hotel_results: HotelSearchResult | None = Field(None, description="Hotel search options")
    weather_forecast: WeatherResult | None = Field(None, description="Destination weather forecast")
    budget_analysis: BudgetAnalysis | None = Field(None, description="Financial budget analysis")
    itinerary: Itinerary | None = Field(None, description="Day-by-day itinerary")
    is_demo: bool = Field(True, description="Demo mode indicator")


class HITLActionRequest(BaseModel):
    """Request payload for Human-in-the-Loop approval/edit/reject actions."""

    feedback: str | None = Field("", description="User feedback or revision instructions")


class SessionDetailResponse(BaseModel):
    """Detailed session state query response."""

    session_id: str = Field(..., description="Session identifier")
    request_id: str = Field(..., description="Request identifier")
    user_query: str = Field(..., description="Original user prompt")
    destination: str | None = Field(None, description="Destination city")
    origin: str | None = Field(None, description="Origin city")
    approval_status: str = Field(..., description="Current approval status")
    human_feedback: str | None = Field(None, description="User feedback text")
    final_response: str | None = Field(None, description="Synthesized response")
    state: dict[str, Any] | None = Field(None, description="Full checkpointed TravelState")
    created_at: str = Field(..., description="ISO creation timestamp")
