"""SQLAlchemy Database Models for Sessions and Workflow Memory."""

from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, String, Text

from backend.app.models.database import Base


class TravelSessionModel(Base):
    """Database model for persisting user travel sessions and checkpointed state."""

    __tablename__ = "travel_sessions"

    session_id = Column(String(64), primary_key=True, index=True)
    request_id = Column(String(64), nullable=False, index=True)
    user_query = Column(Text, nullable=False)
    destination = Column(String(128), nullable=True)
    origin = Column(String(128), nullable=True)

    approval_status = Column(String(32), default="pending", nullable=False)
    human_feedback = Column(Text, nullable=True)

    state_json = Column(JSON, nullable=True)
    final_response = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
