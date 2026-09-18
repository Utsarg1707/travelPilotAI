"""Unit tests for Supervisor Agent routing logic."""

from backend.app.agents.supervisor import SupervisorAgent
from backend.app.schemas.travel_state import TravelState


def test_supervisor_weather_only_routing():
    state: TravelState = {"user_query": "What is the weather in Dubai next week?"}
    decision = SupervisorAgent.run(state)
    assert decision.destination == "Dubai"
    assert decision.required_agents == ["weather"]
    assert "Weather query detected" in decision.routing_reason


def test_supervisor_flight_only_routing():
    state: TravelState = {"user_query": "Find flights from Bangalore to Dubai."}
    decision = SupervisorAgent.run(state)
    assert decision.origin == "Bangalore"
    assert decision.destination == "Dubai"
    assert decision.required_agents == ["flight"]


def test_supervisor_full_trip_routing():
    state: TravelState = {
        "user_query": "Plan a 5-day trip to Dubai from Bangalore for 2 people with a budget of ₹1,50,000."
    }
    decision = SupervisorAgent.run(state)
    assert decision.destination == "Dubai"
    assert decision.origin == "Bangalore"
    assert decision.duration_days == 5
    assert decision.travelers == 2
    assert decision.constraints.get("budget") == 150000.0
    assert len(decision.required_agents) == 5


def test_supervisor_multi_destination_routing():
    state: TravelState = {
        "user_query": "Plan a 7-day trip to Dubai and Abu Dhabi from Bangalore for 2 travelers."
    }
    decision = SupervisorAgent.run(state)
    assert len(decision.destinations) == 2
    assert "Dubai" in decision.destinations
    assert "Abu Dhabi" in decision.destinations
    assert decision.origin == "Bangalore"
    assert decision.duration_days == 7
    assert len(decision.required_agents) == 5
