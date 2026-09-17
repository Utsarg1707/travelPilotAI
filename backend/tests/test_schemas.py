"""Unit tests for Pydantic Schemas and TravelState."""

from backend.app.schemas import (
    BudgetAnalysis,
    CostBreakdown,
    FlightOption,
    FlightSearchResult,
    HotelOption,
    HotelSearchResult,
    SupervisorDecision,
    TravelState,
)


def test_flight_search_schema():
    opt = FlightOption(
        airline="IndiGo",
        flight_number="6E-101",
        departure_time="08:00 AM",
        arrival_time="11:30 AM",
        origin="BLR",
        destination="DXB",
        price_inr=15000.0,
        total_price_inr=30000.0,
        duration="4h 00m",
        is_demo=True,
    )
    result = FlightSearchResult(
        origin="BLR",
        destination="DXB",
        travelers=2,
        total_options=1,
        options=[opt],
        cheapest_option=opt,
    )
    assert result.total_options == 1
    assert result.is_demo is True
    assert "simulated" in result.note


def test_hotel_search_schema():
    opt = HotelOption(
        hotel_name="Marina View Hotel",
        rating=4.5,
        location="Dubai Marina",
        price_per_night_inr=8000.0,
        total_price_inr=32000.0,
        amenities=["Pool", "WiFi"],
        is_demo=True,
    )
    result = HotelSearchResult(
        destination="Dubai",
        nights=4,
        total_options=1,
        options=[opt],
        best_rated=opt,
    )
    assert result.total_options == 1
    assert result.options[0].hotel_name == "Marina View Hotel"


def test_budget_analysis_schema():
    breakdown = CostBreakdown(
        flights=30000.0,
        accommodation=32000.0,
        food=15000.0,
        transport=10000.0,
        activities=15000.0,
        miscellaneous=5000.0,
    )
    analysis = BudgetAnalysis(
        estimated_total=107000.0,
        budget_limit=150000.0,
        remaining_budget=43000.0,
        within_budget=True,
        cost_breakdown=breakdown,
        recommendations=["Great job staying within budget!"],
        status_label="Within Budget",
    )
    assert analysis.within_budget is True
    assert analysis.remaining_budget == 43000.0


def test_supervisor_decision_schema():
    decision = SupervisorDecision(
        destination="Dubai",
        origin="Bangalore",
        travelers=2,
        duration_days=5,
        required_agents=["flight", "hotel", "weather", "budget", "itinerary"],
        routing_reason="Full itinerary plan requested",
    )
    assert len(decision.required_agents) == 5
    assert decision.destination == "Dubai"


def test_travel_state_structure():
    state: TravelState = {
        "session_id": "sess_123",
        "request_id": "req_456",
        "user_query": "Plan a 5-day trip to Dubai",
        "selected_agents": ["flight", "hotel"],
        "errors": [],
        "warnings": [],
        "graph_iteration_count": 1,
    }
    assert state["session_id"] == "sess_123"
    assert len(state["selected_agents"]) == 2
