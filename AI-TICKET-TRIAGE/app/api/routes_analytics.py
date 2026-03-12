from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.ticket import Ticket
from app.models.feedback import Feedback

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    total = db.query(func.count(Ticket.id)).scalar()
    by_category = dict(
        db.query(Ticket.category, func.count(Ticket.id))
        .group_by(Ticket.category).all()
    )
    by_urgency = dict(
        db.query(Ticket.urgency, func.count(Ticket.id))
        .group_by(Ticket.urgency).all()
    )
    by_team = dict(
        db.query(Ticket.assigned_team, func.count(Ticket.id))
        .group_by(Ticket.assigned_team).all()
    )
    avg_confidence = db.query(func.avg(Ticket.confidence)).scalar()
    avg_latency = db.query(func.avg(Ticket.processing_time_ms)).scalar()
    total_feedback = db.query(func.count(Feedback.id)).scalar()
    category_overrides = (
        db.query(func.count(Feedback.id))
        .filter(Feedback.corrected_category.isnot(None))
        .scalar()
    )
    return {
        "total_tickets": total,
        "by_category": by_category,
        "by_urgency": by_urgency,
        "by_team": by_team,
        "avg_confidence": round(avg_confidence or 0, 3),
        "avg_latency_ms": round(avg_latency or 0, 1),
        "total_feedback": total_feedback,
        "category_override_count": category_overrides,
        "override_rate": round(category_overrides / max(total, 1), 3),
    }