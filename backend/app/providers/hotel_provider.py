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

    def _generate_hotel_options(self, destination: str, nights: int) -> list[HotelOption]:
        dest_clean = destination.strip()
        dest_lower = dest_clean.lower()

        if any(c in dest_lower for c in ["london", "uk"]):
            specs = [
                ("The Westminster Grand Hotel", "Westminster, London", 4.8, 14500.0, "Luxury King Suite", ["Central Heating", "Executive Lounge", "Afternoon Tea", "Free WiFi"]),
                ("Mayfair Boutique Suites", "Mayfair, London", 4.6, 11200.0, "Deluxe Studio", ["Rooftop Terrace", "Gym", "Free WiFi"]),
                ("Covent Garden Heritage Inn", "Covent Garden, London", 4.4, 8800.0, "Classic Double Room", ["Historic Dining", "Free Breakfast", "WiFi"]),
            ]
        elif any(c in dest_lower for c in ["paris", "france"]):
            specs = [
                ("Le Marais Grand Palace", "Le Marais, Paris", 4.9, 16000.0, "Eiffel View Suite", ["Spa", "Michelin Dining", "Free WiFi"]),
                ("Saint-Germain Boutique Hotel", "Saint-Germain-des-Prés, Paris", 4.5, 12000.0, "Executive Room", ["Wine Cellar", "Garden Courtyard"]),
                ("Montmartre Heritage Suites", "Montmartre, Paris", 4.3, 8500.0, "Classic French Room", ["Artisan Breakfast", "Free WiFi"]),
            ]
        elif any(c in dest_lower for c in ["shimla", "kashmir", "srinagar", "manali", "gulmarg", "pahalgam"]):
            specs = [
                ("Himalayan Pine & Snow Resort", f"Upper Ridge, {dest_clean}", 4.8, 8500.0, "Mountain View Chalet", ["Fireplace", "Heated Pool", "Spa", "Pahadi Dining"]),
                ("Valley View Heritage Lodge", f"Central Valley, {dest_clean}", 4.5, 5800.0, "Deluxe Cedar Room", ["Bonfire Nights", "Free Breakfast", "WiFi"]),
                ("Snowline Boutique Inn", f"Mall Road, {dest_clean}", 4.3, 4200.0, "Cozy Cottage Room", ["Mountain Balcony", "Tea Lounge"]),
            ]
        elif any(c in dest_lower for c in ["tokyo", "japan", "kyoto"]):
            specs = [
                ("Shinjuku Park Tower Hotel", "Shinjuku, Tokyo", 4.8, 15000.0, "Skyline View Suite", ["Onsen Spa", "Tea Garden", "Free WiFi"]),
                ("Shibuya Crossing Boutique Suites", "Shibuya, Tokyo", 4.5, 9800.0, "Modern Executive Room", ["High-speed Fiber", "Rooftop Bar"]),
                ("Ginza Traditional Ryokan Inn", "Ginza, Tokyo", 4.6, 12500.0, "Tatami Heritage Suite", ["Traditional Kaiseki Breakfast", "Private Bath"]),
            ]
        else:
            specs = [
                (f"Grand Heritage Hotel {dest_clean}", f"Historic Center, {dest_clean}", 4.7, 9500.0, "Deluxe King Room", ["Infinity Pool", "Spa", "Free WiFi", "Breakfast"]),
                (f"City Center Executive Suites {dest_clean}", f"Downtown, {dest_clean}", 4.4, 6500.0, "Executive Suite", ["Rooftop Lounge", "Gym", "Free WiFi"]),
                (f"Boutique Garden Resort {dest_clean}", f"Green Belt, {dest_clean}", 4.3, 5200.0, "Garden Terrace Room", ["Organic Dining", "Free WiFi"]),
            ]

        options: list[HotelOption] = []
        for name, loc, rating, p_night, r_type, amens in specs:
            options.append(
                HotelOption(
                    hotel_name=name,
                    rating=rating,
                    location=loc,
                    price_per_night_inr=p_night,
                    total_price_inr=p_night * nights,
                    amenities=amens,
                    room_type=r_type,
                    is_demo=True,
                )
            )
        return options

    def search_hotels(
        self,
        destination: str,
        nights: int = 4,
        travelers: int = 1,
        max_price_inr: float | None = None,
    ) -> HotelSearchResult:
        options = self._generate_hotel_options(destination, nights)

        if max_price_inr:
            filtered = [h for h in options if h.price_per_night_inr <= max_price_inr]
            if filtered:
                options = filtered

        best_rated = max(options, key=lambda x: x.rating)

        return HotelSearchResult(
            destination=destination,
            nights=nights,
            total_options=len(options),
            options=options,
            best_rated=best_rated,
            is_demo=True,
            note=f"Demo Mode: Accommodation options tailored specifically for {destination}.",
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
