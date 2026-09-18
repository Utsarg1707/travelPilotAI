"""Flight Specialist Agent."""

from backend.app.mcp import MCPClient
from backend.app.providers.flight_provider import DemoFlightProvider
from backend.app.schemas.flights import FlightSearchResult
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
        """Search and compare flight options."""
        provider = DemoFlightProvider()
        return provider.search_flights(origin=origin, destination=destination, travelers=travelers)

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
