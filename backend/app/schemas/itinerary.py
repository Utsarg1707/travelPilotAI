"""Itinerary Schemas."""


from pydantic import BaseModel, Field


class Attraction(BaseModel):
    """Destination attraction / activity reference."""

    name: str = Field(..., description="Attraction or landmark name")
    category: str = Field("General", description="Category (Beach, Cultural, Food, Shopping, Nature)")
    description: str = Field("", description="Brief description")
    estimated_duration: str = Field("2 hours", description="Estimated visit duration")
    estimated_cost_inr: float = Field(0.0, ge=0.0, description="Ticket/entry cost per person in INR")


class ItineraryActivity(BaseModel):
    """Scheduled activity item in day plan."""

    time_slot: str = Field(..., description="Time window (e.g. '09:00 AM - 11:30 AM')")
    activity_title: str = Field(..., description="Activity title")
    description: str = Field(..., description="Detailed activity description")
    location: str = Field(..., description="Venue / address")
    cost_inr: float = Field(0.0, ge=0.0, description="Estimated cost in INR")


class ItineraryDay(BaseModel):
    """Day-by-day itinerary schedule."""

    day_number: int = Field(..., ge=1, description="Day number in trip")
    date: str | None = Field(None, description="Date for this day (YYYY-MM-DD)")
    destination_city: str | None = Field(None, description="City/destination for this specific day")
    theme: str = Field(..., description="Theme for the day (e.g. 'Beach & Coastal Highlights')")
    activities: list[ItineraryActivity] = Field(default_factory=list, description="Scheduled activities")
    daily_cost_inr: float = Field(0.0, ge=0.0, description="Total daily activity expense in INR")


class Itinerary(BaseModel):
    """Complete day-by-day travel plan from Itinerary Agent."""

    destination: str = Field(..., description="Primary or aggregated destination location")
    destinations: list[str] = Field(default_factory=list, description="List of all destinations included in trip")
    total_days: int = Field(..., ge=1, description="Total trip duration in days")
    days: list[ItineraryDay] = Field(default_factory=list, description="Day-by-day itinerary breakdown")
    summary: str = Field(..., description="High-level itinerary summary")
    highlights: list[str] = Field(default_factory=list, description="Top trip highlights")

