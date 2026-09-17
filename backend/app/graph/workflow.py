"""LangGraph StateGraph Definition & Conditional Edge Routing for TravelPilot AI."""

from typing import Any, Literal

from langgraph.graph import END, START, StateGraph

from backend.app.graph.nodes import (
    budget_agent_node,
    flight_agent_node,
    hotel_agent_node,
    human_review_node,
    input_guardrail_node,
    itinerary_agent_node,
    output_guardrail_node,
    supervisor_node,
    weather_agent_node,
)
from backend.app.memory.checkpointer import CheckpointManager
from backend.app.schemas.travel_state import TravelState


def route_input_guardrail(state: TravelState) -> Literal["supervisor", "END"]:
    """Route from input guardrail based on safety and domain checks."""
    guardrail_res = state.get("input_guardrail")
    if guardrail_res and not guardrail_res.allowed:
        return "END"
    return "supervisor"


def route_supervisor(state: TravelState) -> str:
    """Dynamically route from Supervisor to entry specialist agent node."""
    decision = state.get("supervisor_decision")
    if not decision or not decision.required_agents:
        return "output_guardrail"

    selected = decision.required_agents

    if "flight" in selected:
        return "flight_agent"
    if "hotel" in selected:
        return "hotel_agent"
    if "weather" in selected:
        return "weather_agent"
    if "budget" in selected:
        return "budget_agent"
    if "itinerary" in selected:
        return "itinerary_agent"

    return "output_guardrail"


def create_travel_graph(with_checkpointer: bool = True) -> Any:
    """Construct and compile the multi-agent TravelPilot StateGraph workflow."""
    workflow = StateGraph(TravelState)

    # 1. Register Graph Nodes
    workflow.add_node("input_guardrail", input_guardrail_node)
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("flight_agent", flight_agent_node)
    workflow.add_node("hotel_agent", hotel_agent_node)
    workflow.add_node("weather_agent", weather_agent_node)
    workflow.add_node("budget_agent", budget_agent_node)
    workflow.add_node("itinerary_agent", itinerary_agent_node)
    workflow.add_node("output_guardrail", output_guardrail_node)
    workflow.add_node("human_review", human_review_node)

    # 2. Add Workflow Edges
    workflow.add_edge(START, "input_guardrail")

    workflow.add_conditional_edges(
        "input_guardrail",
        route_input_guardrail,
        {
            "supervisor": "supervisor",
            "END": END,
        },
    )

    workflow.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "flight_agent": "flight_agent",
            "hotel_agent": "hotel_agent",
            "weather_agent": "weather_agent",
            "budget_agent": "budget_agent",
            "itinerary_agent": "itinerary_agent",
            "output_guardrail": "output_guardrail",
        },
    )

    # Sequential workflow pipeline
    workflow.add_edge("flight_agent", "hotel_agent")
    workflow.add_edge("hotel_agent", "weather_agent")
    workflow.add_edge("weather_agent", "budget_agent")
    workflow.add_edge("budget_agent", "itinerary_agent")
    workflow.add_edge("itinerary_agent", "output_guardrail")
    workflow.add_edge("output_guardrail", "human_review")
    workflow.add_edge("human_review", END)

    checkpointer = CheckpointManager.get_checkpointer() if with_checkpointer else None
    return workflow.compile(checkpointer=checkpointer)
