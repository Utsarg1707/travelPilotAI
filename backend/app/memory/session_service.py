"""Session Memory Service for DB operations and state serialization."""

from typing import Any

from sqlalchemy.orm import Session

from backend.app.models.database import SessionLocal, init_db
from backend.app.models.session import TravelSessionModel


class SessionService:
    """Service handling session persistence, retrieval, and updates."""

    @classmethod
    def save_session(
        cls,
        session_id: str,
        request_id: str,
        user_query: str,
        destination: str | None = None,
        origin: str | None = None,
        approval_status: str = "pending",
        human_feedback: str | None = None,
        state_dict: dict[str, Any] | None = None,
        final_response: str | None = None,
        db: Session | None = None,
    ) -> TravelSessionModel:
        """Create or update travel session in database."""
        init_db()
        session_created = False
        if db is None:
            db = SessionLocal()
            session_created = True

        try:
            record = db.query(TravelSessionModel).filter(TravelSessionModel.session_id == session_id).first()
            if not record:
                record = TravelSessionModel(
                    session_id=session_id,
                    request_id=request_id,
                    user_query=user_query,
                    destination=destination,
                    origin=origin,
                    approval_status=approval_status,
                    human_feedback=human_feedback,
                    state_json=state_dict,
                    final_response=final_response,
                )
                db.add(record)
            else:
                record.user_query = user_query or record.user_query
                record.destination = destination or record.destination
                record.origin = origin or record.origin
                record.approval_status = approval_status or record.approval_status
                record.human_feedback = human_feedback or record.human_feedback
                if state_dict is not None:
                    record.state_json = state_dict
                if final_response is not None:
                    record.final_response = final_response

            db.commit()
            db.refresh(record)
            return record
        finally:
            if session_created:
                db.close()

    @classmethod
    def get_session(cls, session_id: str, db: Session | None = None) -> TravelSessionModel | None:
        """Fetch travel session by session_id."""
        init_db()
        session_created = False
        if db is None:
            db = SessionLocal()
            session_created = True

        try:
            return db.query(TravelSessionModel).filter(TravelSessionModel.session_id == session_id).first()
        finally:
            if session_created:
                db.close()
