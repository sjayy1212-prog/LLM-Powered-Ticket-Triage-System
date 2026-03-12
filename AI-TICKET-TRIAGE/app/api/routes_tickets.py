from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud
from app.schemas.ticket import TicketInput, TicketOutput
from core.pipeline import run_triage

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/", response_model=TicketOutput)
def create_and_triage_ticket(payload: TicketInput, db: Session = Depends(get_db)):
    result = run_triage(subject=payload.subject, body=payload.body)
    ticket = crud.create_ticket(
        db,
        subject=payload.subject,
        body=payload.body,
        customer_email=payload.customer_email,
        category=result["category"],
        urgency=result["urgency"],
        suggested_response=result["suggested_response"],
        assigned_team=result["assigned_team"],
        confidence=result["confidence"],
        processing_time_ms=result["processing_time_ms"],
        model_used=result["model_used"],
    )
    return ticket


@router.get("/{ticket_id}", response_model=TicketOutput)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = crud.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.get("/", response_model=list[TicketOutput])
def list_tickets(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_tickets(db, skip=skip, limit=limit)