from pydantic import BaseModel, Field
from datetime import datetime


class TicketInput(BaseModel):
    subject: str | None = None
    body: str = Field(..., min_length=5, max_length=5000)
    customer_email: str | None = None


class TicketOutput(BaseModel):
    id: str
    created_at: datetime
    subject: str | None
    body: str
    customer_email: str | None

    category: str | None
    urgency: str | None
    suggested_response: str | None
    assigned_team: str | None
    confidence: float | None
    processing_time_ms: float | None
    model_used: str | None
    status: str

    class Config:
        from_attributes = True
        protected_namespaces = ()


class TriageResult(BaseModel):
    category: str
    urgency: str
    suggested_response: str
    assigned_team: str
    confidence: float
    similar_tickets: list[str] = []