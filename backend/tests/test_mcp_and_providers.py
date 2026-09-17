"""Unit tests for Provider Abstractions and MCP Tool Calling."""

from backend.app.mcp import MCPClient
from backend.app.providers import DemoFlightProvider, DemoHotelProvider, FreeWeatherProvider


def test_demo_flight_provider():
    provider = DemoFlightProvider()
    res = provider.search_flights("BLR", "DXB", 2)
    assert res.total_options == 3
    assert res.cheapest_option is not None
    assert res.is_demo is True

    details = provider.get_flight_details("EK-565")
    assert details["flight_number"] == "EK-565"


def test_demo_hotel_provider():
    provider = DemoHotelProvider()
    res = provider.search_hotels("Dubai", nights=4)
    assert res.total_options == 3
    assert res.best_rated is not None
    assert res.is_demo is True


def test_free_weather_provider():
    provider = FreeWeatherProvider()
    res = provider.get_weather_forecast("Dubai", days=5)
    assert res.destination == "Dubai"
    assert len(res.forecast) == 5


def test_mcp_client_tool_call_allowlist_pass():
    success, data, info = MCPClient.call_tool(
        agent_name="FlightAgent",
        tool_name="search_flights",
        arguments={"origin": "BLR", "destination": "DXB", "travelers": 2},
    )
    assert success is True
    assert data["total_options"] == 3
    assert info.agent_name == "FlightAgent"
    assert info.tool_name == "search_flights"
    assert info.execution_time_ms >= 0.0


def test_mcp_client_tool_call_blocked_if_not_allowlisted():
    success, data, info = MCPClient.call_tool(
        agent_name="MaliciousAgent",
        tool_name="unauthorized_exec_shell",
        arguments={"command": "dir"},
    )
    assert success is False
    assert data is None
    assert "not in allowlist" in info.result_summary
