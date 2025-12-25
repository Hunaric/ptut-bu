from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.calendar_event import CalendarEvent
from app.schemas.calendar import CalendarEventCreate, CalendarEventUpdate
from uuid import UUID

def create_event(db: Session, data: CalendarEventCreate, user_id: UUID):
    event = CalendarEvent(
        user_id=user_id,
        title=data.title,
        start_date=data.start_date,
        end_date=data.end_date,
        level=data.level,
        type="custom"
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_events(db: Session, user_id: UUID):
    return db.query(CalendarEvent).filter(
        CalendarEvent.user_id == user_id
    ).all()

def update_event(db: Session, event_id: int, data: CalendarEventUpdate, user_id: UUID):
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.user_id == user_id,
        CalendarEvent.type == "custom"
    ).first()

    if not event:
        raise HTTPException(404, "Event not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(event, field, value)

    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, event_id: int, user_id: UUID):
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.user_id == user_id,
        CalendarEvent.type == "custom"
    ).first()

    if not event:
        raise HTTPException(404, "Event not found")

    db.delete(event)
    db.commit()
