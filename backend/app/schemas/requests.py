"""Normalized Travel Request Schemas."""

from typing import Any

from pydantic import BaseModel, Field


class TravelDates(BaseModel):
    """Travel dates representation."""

    start_date: str | None = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: str | None = Field(None, description="End date (YYYY-MM-DD)")
    duration_days: int = Field(1, ge=1, description="Total trip duration in days")


class NormalizedTravelRequest(BaseModel):
    """Clean, structured representation of user travel request."""

    origin: str = Field(..., description="Origin city or airport code")
    destination: str = Field(..., description="Destination city or airport code")
    duration_days: int = Field(1, ge=1, description="Trip duration in days")
    travelers: int = Field(1, ge=1, description="Number of travelers")
    budget: float = Field(0.0, ge=0.0, description="Total travel budget in INR")
    preferences: list[str] = Field(default_factory=list, description="User travel preferences")
    constraints: dict[str, Any] = Field(default_factory=dict, description="Additional constraints")
