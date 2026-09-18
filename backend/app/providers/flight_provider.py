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

    def _select_airlines(self, destination: str) -> list[tuple[str, str, float, str]]:
        dest_lower = destination.lower()
        if any(c in dest_lower for c in ["london", "uk", "manchester", "edinburgh"]):
            return [
                ("British Airways", "BA-118", 42000.0, "10h 15m"),
                ("Air India", "AI-177", 38500.0, "10h 30m"),
                ("Virgin Atlantic", "VS-317", 45000.0, "10h 10m"),
            ]
        elif any(c in dest_lower for c in ["paris", "rome", "barcelona", "amsterdam", "zurich", "berlin", "madrid"]):
            return [
                ("Air France", "AF-191", 41000.0, "9h 45m"),
                ("Lufthansa", "LH-755", 39500.0, "10h 00m"),
                ("Air India", "AI-143", 36000.0, "10h 15m"),
            ]
        elif any(c in dest_lower for c in ["tokyo", "japan", "seoul", "singapore", "bali", "bangkok", "thailand"]):
            return [
                ("Singapore Airlines", "SQ-503", 32000.0, "4h 30m"),
                ("Japan Airlines", "JL-754", 48000.0, "9h 20m"),
                ("IndiGo", "6E-1053", 24000.0, "4h 45m"),
            ]
        elif any(c in dest_lower for c in ["new york", "usa", "canada", "toronto", "san francisco"]):
            return [
                ("Air India", "AI-101", 62000.0, "16h 00m"),
                ("United Airlines", "UA-868", 68000.0, "16h 30m"),
                ("Emirates", "EK-201", 71000.0, "18h 15m"),
            ]
        elif any(c in dest_lower for c in ["dubai", "abu dhabi", "qatar", "doha", "sharjah"]):
            return [
                ("Emirates", "EK-565", 18500.0, "4h 00m"),
                ("IndiGo", "6E-1401", 14200.0, "4h 00m"),
                ("Air India", "AI-995", 16100.0, "4h 10m"),
            ]
        else:
            return [
                ("IndiGo", "6E-241", 6500.0, "2h 15m"),
                ("Air India", "AI-504", 7200.0, "2h 30m"),
                ("Akasa Air", "QP-112", 5800.0, "2h 20m"),
            ]

    def search_flights(
        self,
        origin: str,
        destination: str,
        travelers: int = 1,
        departure_date: str | None = None,
    ) -> FlightSearchResult:
        airline_data = self._select_airlines(destination)
        times = [("10:30 AM", "08:45 PM"), ("06:15 AM", "04:30 PM"), ("04:30 PM", "02:40 AM")]

        options: list[FlightOption] = []
        for idx, (carrier, code, base_price, dur) in enumerate(airline_data):
            dep, arr = times[idx % len(times)]
            options.append(
                FlightOption(
                    airline=carrier,
                    flight_number=code,
                    departure_time=dep,
                    arrival_time=arr,
                    origin=origin,
                    destination=destination,
                    price_inr=base_price,
                    total_price_inr=base_price * travelers,
                    duration=dur,
                    stops=0,
                    is_demo=True,
                )
            )

        cheapest = min(options, key=lambda x: x.price_inr)

        return FlightSearchResult(
            origin=origin,
            destination=destination,
            travelers=travelers,
            total_options=len(options),
            options=options,
            cheapest_option=cheapest,
            is_demo=True,
            note="Demo Mode: Flight results are simulated based on origin and destination region.",
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
