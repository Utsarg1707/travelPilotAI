"""Unit tests for Session Persistence and Checkpointing."""

from backend.app.memory import CheckpointManager, SessionService
from backend.app.models import init_db


def test_checkpoint_manager_singleton():
    cp1 = CheckpointManager.get_checkpointer()
    cp2 = CheckpointManager.get_checkpointer()
    assert cp1 is cp2


def test_session_service_crud():
    init_db()
    sess_id = "test_sess_001"
    req_id = "test_req_001"

    # 1. Create session
    saved = SessionService.save_session(
        session_id=sess_id,
        request_id=req_id,
        user_query="Plan a trip to Paris",
        destination="Paris",
        origin="Bangalore",
        approval_status="pending",
    )
    assert saved.session_id == sess_id
    assert saved.destination == "Paris"

    # 2. Retrieve session
    retrieved = SessionService.get_session(sess_id)
    assert retrieved is not None
    assert retrieved.user_query == "Plan a trip to Paris"

    # 3. Update session
    updated = SessionService.save_session(
        session_id=sess_id,
        request_id=req_id,
        user_query="Plan a trip to Paris",
        approval_status="approved",
        human_feedback="Looks great!",
    )
    assert updated.approval_status == "approved"
    assert updated.human_feedback == "Looks great!"
