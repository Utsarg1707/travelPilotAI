"""Hotel Specialist Agent."""


from backend.app.mcp import MCPClient
from backend.app.schemas.hotels import HotelOption, HotelSearchResult
from backend.app.schemas.travel_state import TravelState


class HotelAgent:
    """Specialist Agent responsible for accommodation search and comparison."""

    @classmethod
    def search(
        cls,
        destination: str = "Dubai",
        nights: int = 4,
        travelers: int = 1,
        preferences: list[str] | None = None,
    ) -> HotelSearchResult:
        """Search and compare accommodation options (Demo Mode provider integration)."""
        options: list[HotelOption] = [
            HotelOption(
                hotel_name=f"Grand Beach Resort {destination}",
                rating=4.7,
                location=f"Central Beachfront, {destination}",
                price_per_night_inr=9500.0,
                total_price_inr=9500.0 * nights,
                amenities=["Private Beach", "Infinity Pool", "Spa", "Free WiFi", "Breakfast"],
                room_type="Deluxe Ocean View Room",
                is_demo=True,
            ),
            HotelOption(
                hotel_name=f"City Center Suites {destination}",
                rating=4.3,
                location=f"Downtown, {destination}",
                price_per_night_inr=6200.0,
                total_price_inr=6200.0 * nights,
                amenities=["Rooftop Pool", "Gym", "Free WiFi"],
                room_type="Executive Suite",
                is_demo=True,
            ),
            HotelOption(
                hotel_name=f"Heritage Boutique Hotel {destination}",
                rating=4.5,
                location=f"Historic District, {destination}",
                price_per_night_inr=7800.0,
                total_price_inr=7800.0 * nights,
                amenities=["Cultural Dining", "Garden Terrace", "Free WiFi"],
                room_type="Heritage Room",
                is_demo=True,
            ),
        ]

        best_rated = max(options, key=lambda x: x.rating)

        return HotelSearchResult(
            destination=destination,
            nights=nights,
            total_options=len(options),
            options=options,
            best_rated=best_rated,
            is_demo=True,
            note="Demo Mode: Hotel results are simulated and are not live booking availability.",
        )

    @classmethod
    def run_node(cls, state: TravelState) -> TravelState:
        """Execute Hotel Agent as a LangGraph node handler using MCP tool integration."""
        destination = state.get("destination") or "Dubai"
        duration = state.get("supervisor_decision").duration_days if state.get("supervisor_decision") else 5
        nights = max(1, duration - 1)
        travelers = state.get("travelers") or 1

        success, data, tool_info = MCPClient.call_tool(
            agent_name="HotelAgent",
            tool_name="search_hotels",
            arguments={"destination": destination, "nights": nights, "travelers": travelers},
        )

        result = cls.search(destination=destination, nights=nights, travelers=travelers)
        tool_calls = state.get("tool_calls", []) + [tool_info]

        return {
            "hotel_results": result,
            "tool_calls": tool_calls,
        }

