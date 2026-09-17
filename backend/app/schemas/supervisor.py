"""Supervisor Agent Routing Schemas."""

from typing import Any

from pydantic import BaseModel, Field


class SupervisorDecision(BaseModel):
    """Structured decision output from Supervisor Agent."""

    destination: str = Field(..., description="Destination city/region")
    origin: str = Field("Bangalore", description="Origin city/region")
    travelers: int = Field(1, ge=1, description="Number of travelers")
    duration_days: int = Field(1, ge=1, description="Trip duration in days")
    required_agents: list[str] = Field(
        ...,
        description="List of specialist agent keys required ('flight', 'hotel', 'weather', 'budget', 'itinerary')",
    )
    routing_reason: str = Field(..., description="Concise routing metadata explaining selected agents")
    constraints: dict[str, Any] = Field(default_factory=dict, description="Extracted travel constraints (e.g. budget limit)")
