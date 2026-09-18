"""FastAPI Travel REST API Router."""

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, status
from langgraph.types import Command

from backend.app.graph import create_travel_graph
from backend.app.memory import SessionService
from backend.app.schemas.api import (
    HITLActionRequest,
    PlanRequest,
    PlanResponse,
    SessionDetailResponse,
)
from backend.app.schemas.travel_state import TravelState

router = APIRouter(prefix="/api/v1/travel", tags=["Travel Planning & Decision Support"])


def serialize_state_for_db(state: dict[str, Any]) -> dict[str, Any]:
    """Helper to convert Pydantic objects in TravelState into JSON-serializable dicts."""
    serialized: dict[str, Any] = {}
    for key, val in state.items():
        if hasattr(val, "model_dump"):
            serialized[key] = val.model_dump()
        elif isinstance(val, list):
            serialized[key] = [item.model_dump() if hasattr(item, "model_dump") else item for item in val]
        else:
            serialized[key] = val
    return serialized


@router.post("/plan", response_model=PlanResponse, status_code=status.HTTP_200_OK)
async def create_travel_plan(request: PlanRequest):
    """Submit a travel query and run the multi-agent LangGraph workflow."""
    session_id = request.session_id or f"sess_{uuid.uuid4().hex[:12]}"
    request_id = f"req_{uuid.uuid4().hex[:12]}"

    graph = create_travel_graph(with_checkpointer=True)
    config = {"configurable": {"thread_id": session_id}}

    initial_state: TravelState = {
        "session_id": session_id,
        "request_id": request_id,
        "user_query": request.user_query,
        "graph_iteration_count": 0,
        "errors": [],
        "warnings": [],
        "tool_calls": [],
    }

    try:
        # Stream initial graph run up to output guardrail / HITL interrupt
        list(graph.stream(initial_state, config))
        state_snap = graph.get_state(config)
        current_values = state_snap.values or {}

        status_str = "waiting_for_approval" if "human_review" in (state_snap.next or []) else "completed"
        if current_values.get("input_guardrail") and not current_values.get("input_guardrail").allowed:
            status_str = "blocked"

        db_state = serialize_state_for_db(dict(current_values))

        # Save session to persistent database
        SessionService.save_session(
            session_id=session_id,
            request_id=request_id,
            user_query=request.user_query,
            destination=current_values.get("destination"),
            origin=current_values.get("origin"),
            approval_status=current_values.get("approval_status", "pending"),
            state_dict=db_state,
            final_response=current_values.get("final_response"),
        )

        return PlanResponse(
            session_id=session_id,
            request_id=request_id,
            status=status_str,
            approval_status=current_values.get("approval_status", "pending"),
            supervisor_decision=current_values.get("supervisor_decision"),
            selected_agents=current_values.get("selected_agents", []),
            final_response=current_values.get("final_response"),
            tool_calls=current_values.get("tool_calls", []),
            flight_results=current_values.get("flight_results"),
            hotel_results=current_values.get("hotel_results"),
            weather_forecast=current_values.get("weather_results"),
            budget_analysis=current_values.get("budget_analysis"),
            itinerary=current_values.get("itinerary"),
            is_demo=True,
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing travel workflow: {err!s}",
        )


@router.get("/{session_id}", response_model=SessionDetailResponse)
async def get_session_details(session_id: str):
    """Retrieve existing travel plan session status and checkpoint details."""
    record = SessionService.get_session(session_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session '{session_id}' not found.",
        )

    return SessionDetailResponse(
        session_id=record.session_id,
        request_id=record.request_id,
        user_query=record.user_query,
        destination=record.destination,
        origin=record.origin,
        approval_status=record.approval_status,
        human_feedback=record.human_feedback,
        final_response=record.final_response,
        state=record.state_json,
        created_at=record.created_at.isoformat(),
    )


@router.post("/{session_id}/approve", response_model=PlanResponse)
async def approve_plan(session_id: str, request: HITLActionRequest | None = None):
    """Resume interrupted LangGraph execution with APPROVE decision."""
    return await _handle_hitl_resume(session_id=session_id, action="approve", feedback=request.feedback if request else "")


@router.post("/{session_id}/edit", response_model=PlanResponse)
async def edit_plan(session_id: str, request: HITLActionRequest):
    """Resume interrupted LangGraph execution with EDIT decision and user feedback."""
    return await _handle_hitl_resume(session_id=session_id, action="edit", feedback=request.feedback or "")


@router.post("/{session_id}/reject", response_model=PlanResponse)
async def reject_plan(session_id: str, request: HITLActionRequest | None = None):
    """Resume interrupted LangGraph execution with REJECT decision."""
    return await _handle_hitl_resume(session_id=session_id, action="reject", feedback=request.feedback if request else "")


async def _handle_hitl_resume(session_id: str, action: str, feedback: str) -> PlanResponse:
    """Helper method to resume checkpointed graph execution upon human review."""
    record = SessionService.get_session(session_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session '{session_id}' not found.",
        )

    graph = create_travel_graph(with_checkpointer=True)
    config = {"configurable": {"thread_id": session_id}}

    try:
        resume_cmd = Command(resume={"action": action, "feedback": feedback})
        res_state = graph.invoke(resume_cmd, config)
        db_state = serialize_state_for_db(dict(res_state))

        # Update database record
        SessionService.save_session(
            session_id=session_id,
            request_id=record.request_id,
            user_query=record.user_query,
            approval_status=res_state.get("approval_status", action),
            human_feedback=feedback,
            state_dict=db_state,
            final_response=res_state.get("final_response"),
        )

        return PlanResponse(
            session_id=session_id,
            request_id=record.request_id,
            status="completed",
            approval_status=res_state.get("approval_status", action),
            supervisor_decision=res_state.get("supervisor_decision"),
            selected_agents=res_state.get("selected_agents", []),
            final_response=res_state.get("final_response"),
            tool_calls=res_state.get("tool_calls", []),
            flight_results=res_state.get("flight_results"),
            hotel_results=res_state.get("hotel_results"),
            weather_forecast=res_state.get("weather_results"),
            budget_analysis=res_state.get("budget_analysis"),
            itinerary=res_state.get("itinerary"),
            is_demo=True,
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error resuming graph execution: {err!s}",
        )
