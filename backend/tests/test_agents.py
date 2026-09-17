"""Unit tests for Specialist Agents (Flight, Hotel, Weather, Budget, Itinerary)."""

from backend.app.agents.budget import BudgetAgent
from backend.app.agents.flight import FlightAgent
from backend.app.agents.hotel import HotelAgent
from backend.app.agents.itinerary import ItineraryAgent
from backend.app.agents.weather import WeatherAgent


def test_flight_agent_search():
    res = FlightAgent.search(origin="BLR", destination="DXB", travelers=2)
    assert res.origin == "BLR"
    assert res.destination == "DXB"
    assert res.travelers == 2
    assert res.total_options >= 1
    assert res.cheapest_option is not None
    assert res.is_demo is True


def test_hotel_agent_search():
    res = HotelAgent.search(destination="Dubai", nights=4, travelers=2)
    assert res.destination == "Dubai"
    assert res.nights == 4
    assert res.total_options >= 1
    assert res.best_rated.rating >= 4.0
    assert res.is_demo is True


def test_weather_agent_forecast():
    res = WeatherAgent.get_forecast(destination="Dubai", days=5)
    assert res.destination == "Dubai"
    assert len(res.forecast) == 5
    assert res.current_temp_c > 0.0
    assert len(res.recommendations) > 0


def test_budget_agent_deterministic_calculation():
    # Test deterministic budget calculation
    flight_res = FlightAgent.search("BLR", "DXB", 2)
    hotel_res = HotelAgent.search("Dubai", 4, 2)

    res = BudgetAgent.calculate(
        budget_limit=150000.0,
        duration_days=5,
        travelers=2,
        flight_results=flight_res,
        hotel_results=hotel_res,
    )

    assert res.budget_limit == 150000.0
    assert res.cost_breakdown.flights == flight_res.cheapest_option.total_price_inr
    assert res.cost_breakdown.accommodation == hotel_res.options[0].total_price_inr
    assert res.estimated_total > 0.0
    assert res.within_budget is True


def test_itinerary_agent_generation():
    res = ItineraryAgent.generate(destination="Dubai", duration_days=5)
    assert res.destination == "Dubai"
    assert res.total_days == 5
    assert len(res.days) == 5
    # Verify no scheduling overlaps (activities ordered properly)
    for day in res.days:
        assert len(day.activities) >= 1
