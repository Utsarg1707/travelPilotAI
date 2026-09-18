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
        "destinations": decision.destinations,
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


def synthesize_partial_response(state: TravelState) -> str:
    """Synthesize specific markdown response when ItineraryAgent is skipped."""
    selected = state.get("selected_agents") or []
    origin = state.get("origin") or "Bangalore"
    destination = state.get("destination") or "Destination"
    travelers = state.get("travelers") or 1

    lines: list[str] = []

    if "flight" in selected and state.get("flight_results"):
        f_res = state.get("flight_results")
        lines.append(f"# ✈️ Flight Search Results: {origin} to {destination}")
        lines.append(
            f"**Origin**: {origin} | **Destination**: {destination} | **Travelers**: {travelers}\n"
        )
        if f_res and f_res.options:
            lines.append(
                "| Airline | Flight No | Departure | Arrival | Duration | Price / Person | Total Flight Cost |"
            )
            lines.append("|---|---|---|---|---|---|---|")
            for f in f_res.options:
                lines.append(
                    f"| **{f.airline}** | `{f.flight_number}` | {f.departure_time} | {f.arrival_time} | {f.duration} | ₹{f.price_inr:,.2f} | **₹{f.total_price_inr:,.2f}** |"
                )
        lines.append(
            "\n*Demo Mode: Flight results are simulated and are not live booking availability.*"
        )
        return "\n".join(lines)

    if "hotel" in selected and state.get("hotel_results"):
        h_res = state.get("hotel_results")
        lines.append(f"# 🏨 Accommodation Options in {destination}")
        lines.append(
            f"**Destination**: {destination} | **Nights**: {h_res.nights if h_res else 1}\n"
        )
        if h_res and h_res.options:
            lines.append(
                "| Hotel Name | Location | Rating | Price / Night | Total Stay | Key Amenities |"
            )
            lines.append("|---|---|---|---|---|---|")
            for h in h_res.options:
                amenities_str = ", ".join(h.amenities[:3]) if h.amenities else "WiFi, AC, Breakfast"
                lines.append(
                    f"| **{h.hotel_name}** | {h.location} | ⭐ {h.rating}/5 | ₹{h.price_per_night_inr:,.2f} | **₹{h.total_price_inr:,.2f}** | {amenities_str} |"
                )
        lines.append(
            "\n*Demo Mode: Hotel results are simulated and are not live booking availability.*"
        )
        return "\n".join(lines)

    if "weather" in selected and state.get("weather_results"):
        w_res = state.get("weather_results")
        lines.append(f"# 🌤️ Weather Forecast for {destination}")
        if w_res:
            lines.append(f"**Status**: {w_res.weather_summary}\n")
            if w_res.forecast:
                lines.append("| Day / Date | Max Temp | Min Temp | Condition | Rain Probability |")
                lines.append("|---|---|---|---|---|")
                for w in w_res.forecast:
                    lines.append(
                        f"| {w.date} | {w.temp_max_c:.1f}°C | {w.temp_min_c:.1f}°C | {w.weather_condition} | {w.precipitation_prob}% |"
                    )
            if w_res.recommendations:
                lines.append("\n**Recommendations**:")
                for rec in w_res.recommendations:
                    lines.append(f"- {rec}")
        return "\n".join(lines)

    if "budget" in selected and state.get("budget_analysis"):
        b_res = state.get("budget_analysis")
        lines.append(f"# 💰 Budget Analysis for {destination}")
        if b_res:
            lines.append(
                f"**Limit**: ₹{b_res.budget_limit:,.2f} | **Estimated Total**: ₹{b_res.estimated_total:,.2f} | **Status**: `{b_res.status_label}`\n"
            )
            cb = b_res.cost_breakdown
            limit = b_res.budget_limit or 1.0
            lines.append("| Expense Category | Estimated Cost (INR) | % of Budget |")
            lines.append("|---|---|---|")
            lines.append(f"| ✈️ Flights | ₹{cb.flights:,.2f} | {(cb.flights / limit) * 100:.1f}% |")
            lines.append(
                f"| 🏨 Accommodation | ₹{cb.accommodation:,.2f} | {(cb.accommodation / limit) * 100:.1f}% |"
            )
            lines.append(f"| 🍽️ Food & Dining | ₹{cb.food:,.2f} | {(cb.food / limit) * 100:.1f}% |")
            lines.append(
                f"| 🚕 Local Transport | ₹{cb.transport:,.2f} | {(cb.transport / limit) * 100:.1f}% |"
            )
            lines.append(
                f"| 🎟️ Tours & Activities | ₹{cb.activities:,.2f} | {(cb.activities / limit) * 100:.1f}% |"
            )
            lines.append(
                f"| 🛍️ Miscellaneous Buffer | ₹{cb.miscellaneous:,.2f} | {(cb.miscellaneous / limit) * 100:.1f}% |"
            )
            lines.append(
                f"| **TOTAL ESTIMATED** | **₹{b_res.estimated_total:,.2f}** | **{(b_res.estimated_total / limit) * 100:.1f}%** |"
            )
        return "\n".join(lines)

    return "Travel query processed successfully."


def output_guardrail_node(state: TravelState) -> dict[str, Any]:
    """Node handler for validating synthesized output."""
    current_response = state.get("final_response") or synthesize_partial_response(state)
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
            edited_response = (
                f"{state.get('final_response', '')}\n\n### User Revisions Requested:\n{feedback}"
            )
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
