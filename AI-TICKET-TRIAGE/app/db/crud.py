from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.feedback import Feedback


def create_ticket(db: Session, **kwargs) -> Ticket:
    ticket = Ticket(**kwargs)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def get_ticket(db: Session, ticket_id: str) -> Ticket | None:
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def list_tickets(db: Session, skip: int = 0, limit: int = 50) -> list[Ticket]:
    return (
        db.query(Ticket)
        .order_by(Ticket.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_ticket(db: Session, ticket_id: str, **kwargs) -> Ticket | None:
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        return None
    for k, v in kwargs.items():
        setattr(ticket, k, v)
    db.commit()
    db.refresh(ticket)
    return ticket


def create_feedback(db: Session, **kwargs) -> Feedback:
    fb = Feedback(**kwargs)
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb


def get_feedback_for_ticket(db: Session, ticket_id: str) -> list[Feedback]:
    return db.query(Feedback).filter(Feedback.ticket_id == ticket_id).all()


def get_all_feedback(db: Session, limit: int = 200) -> list[Feedback]:
    return (
        db.query(Feedback)
        .order_by(Feedback.created_at.desc())
        .limit(limit)
        .all()
    )