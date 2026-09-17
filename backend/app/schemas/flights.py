"""Flight Search Schemas."""


from pydantic import BaseModel, Field


class FlightOption(BaseModel):
    """Single flight option details."""

    airline: str = Field(..., description="Airline name")
    flight_number: str = Field(..., description="Flight designation")
    departure_time: str = Field(..., description="Departure timestamp or time")
    arrival_time: str = Field(..., description="Arrival timestamp or time")
    origin: str = Field(..., description="Origin airport/city")
    destination: str = Field(..., description="Destination airport/city")
    price_inr: float = Field(..., ge=0.0, description="Price per seat in INR")
    total_price_inr: float = Field(0.0, ge=0.0, description="Total flight cost for all travelers in INR")
    duration: str = Field(..., description="Flight duration string (e.g. '4h 15m')")
    stops: int = Field(0, ge=0, description="Number of layover stops")
    is_demo: bool = Field(True, description="Indicates if flight result is simulated demo data")


class FlightSearchResult(BaseModel):
    """Aggregate search results from Flight Agent."""

    origin: str = Field(..., description="Origin location")
    destination: str = Field(..., description="Destination location")
    travelers: int = Field(1, ge=1, description="Number of passengers")
    total_options: int = Field(0, ge=0, description="Count of options found")
    options: list[FlightOption] = Field(default_factory=list, description="Available flight options")
    cheapest_option: FlightOption | None = Field(None, description="Cheapest flight option")
    is_demo: bool = Field(True, description="Demo mode indicator")
    note: str = Field(
        "Demo Mode: Flight results are simulated and are not live booking availability.",
        description="User-facing status note",
    )
