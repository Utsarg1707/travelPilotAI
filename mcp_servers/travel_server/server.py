"""MCP Travel Server providing search_attractions and get_destination_info tools."""

from typing import Any, Dict, List


def search_attractions(destination: str) -> List[Dict[str, Any]]:
    """MCP Tool: Search top attractions in destination."""
    return [
        {
            "name": f"{destination} Beach Promenade",
            "category": "Beach & Leisure",
            "description": f"Famous scenic coastal walking path in {destination}.",
            "estimated_duration": "2 hours",
            "estimated_cost_inr": 0.0,
        },
        {
            "name": f"{destination} Cultural Heritage Souk",
            "category": "Culture & Shopping",
            "description": "Historic traditional market with spices and handicrafts.",
            "estimated_duration": "3 hours",
            "estimated_cost_inr": 1000.0,
        },
        {
            "name": f"{destination} Skyline Observation Deck",
            "category": "Sightseeing",
            "description": "Panoramic panoramic views across the city skyline.",
            "estimated_duration": "1.5 hours",
            "estimated_cost_inr": 2500.0,
        },
    ]


def get_destination_info(destination: str) -> Dict[str, Any]:
    """MCP Tool: Get destination travel tips and visa/currency metadata."""
    return {
        "destination": destination,
        "primary_language": "English / Local",
        "currency": "AED / EUR / JPY / Local",
        "time_zone": "GMT+4",
        "emergency_number": "112 / 999",
        "transport_tips": "Taxis, Metro, and rideshare apps widely available.",
    }
