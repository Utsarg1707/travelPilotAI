"""Hotel Search Schemas."""

from pydantic import BaseModel, Field


class HotelOption(BaseModel):
    """Single accommodation option details."""

    hotel_name: str = Field(..., description="Name of hotel/resort")
    rating: float = Field(..., ge=0.0, le=5.0, description="User rating out of 5.0")
    location: str = Field(..., description="Neighborhood or area location")
    price_per_night_inr: float = Field(..., ge=0.0, description="Nightly rate in INR")
    total_price_inr: float = Field(..., ge=0.0, description="Total stay cost in INR")
    amenities: list[str] = Field(default_factory=list, description="Key hotel amenities")
    room_type: str = Field("Standard Room", description="Room type description")
    is_demo: bool = Field(True, description="Indicates if hotel result is simulated demo data")


class HotelSearchResult(BaseModel):
    """Aggregate search results from Hotel Agent."""

    destination: str = Field(..., description="Destination location")
    check_in: str | None = Field(None, description="Check-in date")
    check_out: str | None = Field(None, description="Check-out date")
    nights: int = Field(1, ge=1, description="Number of nights")
    total_options: int = Field(0, ge=0, description="Count of hotel options found")
    options: list[HotelOption] = Field(default_factory=list, description="Available hotel options")
    best_rated: HotelOption | None = Field(None, description="Highest rated hotel option")
    is_demo: bool = Field(True, description="Demo mode indicator")
    note: str = Field(
        "Demo Mode: Hotel results are simulated and are not live booking availability.",
        description="User-facing status note",
    )
