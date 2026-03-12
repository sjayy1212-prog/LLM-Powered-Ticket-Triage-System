from pydantic import BaseModel


class FeedbackInput(BaseModel):
    ticket_id: str
    agent_name: str | None = None
    corrected_category: str | None = None
    corrected_urgency: str | None = None
    corrected_response: str | None = None
    notes: str | None = None


class FeedbackOutput(BaseModel):
    id: str
    ticket_id: str
    original_category: str | None
    corrected_category: str | None
    original_urgency: str | None
    corrected_urgency: str | None
    notes: str | None

    class Config:
        from_attributes = True