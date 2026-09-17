"""Flight Provider Interface and Demo Implementation."""

from abc import ABC, abstractmethod
from typing import Any

from backend.app.schemas.flights import FlightOption, FlightSearchResult


class FlightProvider(ABC):
    """Abstract Base Class for Flight Search Providers."""

    @abstractmethod
    def search_flights(
        self,
        origin: str,
        destination: str,
        travelers: int = 1,
        departure_date: str | None = None,
    ) -> FlightSearchResult:
        """Search flights between origin and destination."""

    @abstractmethod
    def get_flight_details(self, flight_number: str) -> dict[str, Any] | None:
        """Retrieve detailed flight information by flight number."""


class DemoFlightProvider(FlightProvider):
    """Deterministic Demo Flight Provider for offline and free-tier development."""

    def search_flights(
        self,
        origin: str,
        destination: str,
        travelers: int = 1,
        departure_date: str | None = None,
    ) -> FlightSearchResult:
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

    def get_flight_details(self, flight_number: str) -> dict[str, Any] | None:
        return {
            "flight_number": flight_number,
            "aircraft": "Boeing 777-300ER / Airbus A320neo",
            "baggage_allowance": "30 kg checked, 7 kg cabin",
            "in_flight_meal": "Included",
            "cancellation_policy": "Refundable with fee",
            "is_demo": True,
        }
