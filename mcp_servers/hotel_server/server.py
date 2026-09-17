"""MCP Hotel Server providing search_hotels and get_hotel_details tools."""

from typing import Any, Dict
from backend.app.providers.hotel_provider import DemoHotelProvider

provider = DemoHotelProvider()


def search_hotels(destination: str, nights: int = 4, travelers: int = 1) -> Dict[str, Any]:
    """MCP Tool: Search hotel options in destination."""
    res = provider.search_hotels(destination=destination, nights=nights, travelers=travelers)
    return res.model_dump()


def get_hotel_details(hotel_name: str) -> Dict[str, Any]:
    """MCP Tool: Get detailed hotel policies and amenity info."""
    res = provider.get_hotel_details(hotel_name=hotel_name)
    return res or {}
