import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from app.db.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id = Column(String, ForeignKey("tickets.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    agent_name = Column(String(255), nullable=True)

    original_category = Column(String(50))
    original_urgency = Column(String(20))
    original_response = Column(Text)

    corrected_category = Column(String(50), nullable=True)
    corrected_urgency = Column(String(20), nullable=True)
    corrected_response = Column(Text, nullable=True)

    notes = Column(Text, nullable=True)