import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, Float
from app.db.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    subject = Column(String(500), nullable=True)
    body = Column(Text, nullable=False)
    customer_email = Column(String(255), nullable=True)

    category = Column(String(50), nullable=True)
    urgency = Column(String(20), nullable=True)
    suggested_response = Column(Text, nullable=True)
    assigned_team = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=True)

    processing_time_ms = Column(Float, nullable=True)
    model_used = Column(String(100), nullable=True)
    status = Column(String(20), default="open")