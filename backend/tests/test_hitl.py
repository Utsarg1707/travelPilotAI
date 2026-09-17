"""Unit tests for LangGraph Human-in-the-Loop (HITL) Interrupt and Resume."""

from langgraph.types import Command

from backend.app.graph import create_travel_graph
from backend.app.schemas.travel_state import TravelState


def test_hitl_interrupt_and_approve():
    graph = create_travel_graph(with_checkpointer=True)
    config = {"configurable": {"thread_id": "thread_hitl_approve_001"}}

    initial_state: TravelState = {
        "session_id": "sess_hitl_001",
        "request_id": "req_hitl_001",
        "user_query": "Plan a 5-day trip to Dubai from Bangalore for 2 people with a budget of ₹1,50,000.",
    }

    # 1. First invocation triggers interrupt at human_review node
    events = list(graph.stream(initial_state, config))
    state_snap = graph.get_state(config)
    assert len(state_snap.next) > 0
    assert "human_review" in state_snap.next[0]

    # 2. Resume with APPROVE action
    resume_cmd = Command(resume={"action": "approve", "feedback": "Looks great!"})
    res_final = graph.invoke(resume_cmd, config)

    assert res_final.get("approval_status") == "approved"
    assert res_final.get("is_completed") is True


def test_hitl_interrupt_and_edit():
    graph = create_travel_graph(with_checkpointer=True)
    config = {"configurable": {"thread_id": "thread_hitl_edit_002"}}

    initial_state: TravelState = {
        "session_id": "sess_hitl_002",
        "request_id": "req_hitl_002",
        "user_query": "Plan a 5-day trip to Dubai from Bangalore for 2 people with a budget of ₹1,50,000.",
    }

    # 1. Trigger interrupt
    list(graph.stream(initial_state, config))

    # 2. Resume with EDIT action
    resume_cmd = Command(resume={"action": "edit", "feedback": "Please choose a cheaper resort near downtown."})
    res_final = graph.invoke(resume_cmd, config)

    assert res_final.get("approval_status") == "edited"
    assert "cheaper resort" in res_final.get("human_feedback")
    assert "User Revisions Requested" in res_final.get("final_response")


def test_hitl_interrupt_and_reject():
    graph = create_travel_graph(with_checkpointer=True)
    config = {"configurable": {"thread_id": "thread_hitl_reject_003"}}

    initial_state: TravelState = {
        "session_id": "sess_hitl_003",
        "request_id": "req_hitl_003",
        "user_query": "Plan a 5-day trip to Dubai from Bangalore for 2 people with a budget of ₹1,50,000.",
    }

    # 1. Trigger interrupt
    list(graph.stream(initial_state, config))

    # 2. Resume with REJECT action
    resume_cmd = Command(resume={"action": "reject", "feedback": "Budget is too high."})
    res_final = graph.invoke(resume_cmd, config)

    assert res_final.get("approval_status") == "rejected"
    assert "rejected by user" in res_final.get("final_response")
