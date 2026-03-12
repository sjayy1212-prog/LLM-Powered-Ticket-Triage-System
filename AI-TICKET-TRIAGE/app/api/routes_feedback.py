from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud
from app.schemas.feedback import FeedbackInput, FeedbackOutput

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/", response_model=FeedbackOutput)
def submit_feedback(payload: FeedbackInput, db: Session = Depends(get_db)):
    ticket = crud.get_ticket(db, payload.ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    fb = crud.create_feedback(
        db,
        ticket_id=payload.ticket_id,
        agent_name=payload.agent_name,
        original_category=ticket.category,
        original_urgency=ticket.urgency,
        original_response=ticket.suggested_response,
        corrected_category=payload.corrected_category,
        corrected_urgency=payload.corrected_urgency,
        corrected_response=payload.corrected_response,
        notes=payload.notes,
    )
    return fb


@router.get("/", response_model=list[FeedbackOutput])
def list_feedback(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_feedback(db, limit=limit)