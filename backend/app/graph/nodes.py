"""LangGraph Node Handlers for TravelPilot AI Workflow."""

from typing import Any

from langgraph.types import interrupt

from backend.app.agents.budget import BudgetAgent
from backend.app.agents.flight import FlightAgent
from backend.app.agents.hotel import HotelAgent
from backend.app.agents.itinerary import ItineraryAgent
from backend.app.agents.supervisor import SupervisorAgent
from backend.app.agents.weather import WeatherAgent
from backend.app.guardrails import InputGuardrail, OutputGuardrail
from backend.app.schemas.travel_state import TravelState


def input_guardrail_node(state: TravelState) -> dict[str, Any]:
    """Node handler for checking user input safety and domain scope."""
    query = state.get("user_query", "")
    result = InputGuardrail.evaluate(query)

    updates: dict[str, Any] = {
        "input_guardrail": result,
        "graph_iteration_count": state.get("graph_iteration_count", 0) + 1,
    }

    if not result.allowed:
        updates["errors"] = [f"Input Guardrail Blocked: {result.reason}"]
        updates["final_response"] = f"Request Blocked by Safety Guardrail: {result.reason}"
        updates["is_completed"] = True

    return updates


def supervisor_node(state: TravelState) -> dict[str, Any]:
    """Node handler for Supervisor Agent intent analysis and specialist agent selection."""
    decision = SupervisorAgent.run(state)

    return {
        "supervisor_decision": decision,
        "destination": decision.destination,
        "origin": decision.origin,
        "travelers": decision.travelers,
        "budget": decision.constraints.get("budget", 150000.0),
        "selected_agents": decision.required_agents,
        "graph_iteration_count": state.get("graph_iteration_count", 0) + 1,
    }


def flight_agent_node(state: TravelState) -> dict[str, Any]:
    """Node handler for Flight Agent execution."""
    res = FlightAgent.run_node(state)
    res["graph_iteration_count"] = state.get("graph_iteration_count", 0) + 1
    return res


def hotel_agent_node(state: TravelState) -> dict[str, Any]:
    """Node handler for Hotel Agent execution."""
    res = HotelAgent.run_node(state)
    res["graph_iteration_count"] = state.get("graph_iteration_count", 0) + 1
    return res


def weather_agent_node(state: TravelState) -> dict[str, Any]:
    """Node handler for Weather Agent execution."""
    res = WeatherAgent.run_node(state)
    res["graph_iteration_count"] = state.get("graph_iteration_count", 0) + 1
    return res


def budget_agent_node(state: TravelState) -> dict[str, Any]:
    """Node handler for Budget Agent execution."""
    res = BudgetAgent.run_node(state)
    res["graph_iteration_count"] = state.get("graph_iteration_count", 0) + 1
    return res


def itinerary_agent_node(state: TravelState) -> dict[str, Any]:
    """Node handler for Itinerary Agent execution."""
    res = ItineraryAgent.run_node(state)
    res["graph_iteration_count"] = state.get("graph_iteration_count", 0) + 1
    return res


def output_guardrail_node(state: TravelState) -> dict[str, Any]:
    """Node handler for validating synthesized output."""
    current_response = state.get("final_response") or "Travel plan processed successfully."
    result = OutputGuardrail.evaluate(
        final_response=current_response,
        budget_analysis=state.get("budget_analysis"),
        itinerary=state.get("itinerary"),
        is_demo=True,
    )

    return {
        "output_guardrail": result,
        "final_response": result.sanitized_response,
        "approval_status": state.get("approval_status") or "pending",
        "is_completed": True,
        "graph_iteration_count": state.get("graph_iteration_count", 0) + 1,
    }



def human_review_node(state: TravelState) -> dict[str, Any]:
    """Node handler for Human-in-the-Loop review and LangGraph interrupt/resume."""
    current_status = state.get("approval_status", "pending")

    if current_status == "pending":
        # Interrupt workflow execution waiting for human decision
        human_decision = interrupt(
            {
                "message": "Travel plan generated. Waiting for human approval, edit, or rejection.",
                "proposed_plan": state.get("final_response"),
                "session_id": state.get("session_id"),
            }
        )

        # Handle resumed values
        action = human_decision.get("action", "approve").lower()
        feedback = human_decision.get("feedback", "")

        if action == "approve":
            return {
                "approval_status": "approved",
                "human_feedback": feedback,
                "is_completed": True,
            }
        elif action == "edit":
            edited_response = f"{state.get('final_response', '')}\n\n### User Revisions Requested:\n{feedback}"
            return {
                "approval_status": "edited",
                "human_feedback": feedback,
                "final_response": edited_response,
                "is_completed": True,
            }
        elif action == "reject":
            return {
                "approval_status": "rejected",
                "human_feedback": feedback,
                "final_response": "Travel plan was rejected by user.",
                "is_completed": True,
            }

    return {"is_completed": True}
