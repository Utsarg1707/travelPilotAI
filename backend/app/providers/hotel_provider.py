"""Hotel Provider Interface and Demo Implementation."""

from abc import ABC, abstractmethod
from typing import Any

from backend.app.schemas.hotels import HotelOption, HotelSearchResult


class HotelProvider(ABC):
    """Abstract Base Class for Accommodation Search Providers."""

    @abstractmethod
    def search_hotels(
        self,
        destination: str,
        nights: int = 4,
        travelers: int = 1,
        max_price_inr: float | None = None,
    ) -> HotelSearchResult:
        """Search hotels in destination."""

    @abstractmethod
    def get_hotel_details(self, hotel_name: str) -> dict[str, Any] | None:
        """Retrieve detailed hotel amenity & policy information."""


class DemoHotelProvider(HotelProvider):
    """Deterministic Demo Hotel Provider for offline and free-tier development."""

    def search_hotels(
        self,
        destination: str,
        nights: int = 4,
        travelers: int = 1,
        max_price_inr: float | None = None,
    ) -> HotelSearchResult:
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

        if max_price_inr:
            options = [h for h in options if h.price_per_night_inr <= max_price_inr] or options

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

    def get_hotel_details(self, hotel_name: str) -> dict[str, Any] | None:
        return {
            "hotel_name": hotel_name,
            "check_in_time": "03:00 PM",
            "check_out_time": "12:00 PM",
            "cancellation_policy": "Free cancellation up to 48 hours before check-in",
            "breakfast_included": True,
            "shuttle_service": "Available upon request",
            "is_demo": True,
        }
