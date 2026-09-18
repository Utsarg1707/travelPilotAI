"""Flight Specialist Agent."""

from backend.app.mcp import MCPClient
from backend.app.schemas.flights import FlightOption, FlightSearchResult
from backend.app.schemas.travel_state import TravelState


class FlightAgent:
    """Specialist Agent responsible for flight search and option comparison."""

    @classmethod
    def search(
        cls,
        origin: str = "Bangalore",
        destination: str = "Dubai",
        travelers: int = 1,
        preferences: list[str] | None = None,
    ) -> FlightSearchResult:
        """Search and compare flight options (Demo Mode provider integration)."""
        # Generate realistic simulated options tailored to destination
        options: list[FlightOption] = [
            FlightOption(
                airline="Emirates",
                flight_number="EK-565",
                departure_time="10:30 AM",
                arrival_time="01:00 PM",
                origin=origin,
                destination=destination,
                price_inr=18500.0,
                total_price_inr=18500.0 * travelers,
                duration="4h 00m",
                stops=0,
                is_demo=True,
            ),
            FlightOption(
                airline="IndiGo",
                flight_number="6E-1401",
                departure_time="06:15 AM",
                arrival_time="08:45 AM",
                origin=origin,
                destination=destination,
                price_inr=14200.0,
                total_price_inr=14200.0 * travelers,
                duration="4h 00m",
                stops=0,
                is_demo=True,
            ),
            FlightOption(
                airline="Air India",
                flight_number="AI-995",
                departure_time="04:30 PM",
                arrival_time="07:10 PM",
                origin=origin,
                destination=destination,
                price_inr=16100.0,
                total_price_inr=16100.0 * travelers,
                duration="4h 10m",
                stops=0,
                is_demo=True,
            ),
        ]

        # Sort options by price to find cheapest
        cheapest = min(options, key=lambda x: x.price_inr)

        return FlightSearchResult(
            origin=origin,
            destination=destination,
            travelers=travelers,
            total_options=len(options),
            options=options,
            cheapest_option=cheapest,
            is_demo=True,
            note="Demo Mode: Flight results are simulated and are not live booking availability.",
        )

    @classmethod
    def run_node(cls, state: TravelState) -> TravelState:
        """Execute Flight Agent as a LangGraph node handler using MCP tool integration."""
        origin = state.get("origin") or "Bangalore"
        destination = state.get("destination") or "Dubai"
        travelers = state.get("travelers") or 1

        _success, _data, tool_info = MCPClient.call_tool(
            agent_name="FlightAgent",
            tool_name="search_flights",
            arguments={"origin": origin, "destination": destination, "travelers": travelers},
        )

        result = cls.search(origin=origin, destination=destination, travelers=travelers)
        tool_calls = state.get("tool_calls", []) + [tool_info]

        return {
            "flight_results": result,
            "tool_calls": tool_calls,
        }
