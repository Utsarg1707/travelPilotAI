"""MCP Flight Server providing search_flights and get_flight_details tools."""

from typing import Any, Dict
from backend.app.providers.flight_provider import DemoFlightProvider

provider = DemoFlightProvider()


def search_flights(origin: str, destination: str, travelers: int = 1) -> Dict[str, Any]:
    """MCP Tool: Search flight options between origin and destination."""
    res = provider.search_flights(origin=origin, destination=destination, travelers=travelers)
    return res.model_dump()


def get_flight_details(flight_number: str) -> Dict[str, Any]:
    """MCP Tool: Get detailed flight information."""
    res = provider.get_flight_details(flight_number=flight_number)
    return res or {}
