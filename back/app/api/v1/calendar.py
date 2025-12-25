# app/api/calendar.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.calendar import CalendarEventCreate, CalendarEventUpdate, CalendarEventResponse
from app.crud import calendar as crud

router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.get(
    "/events",
    response_model=list[CalendarEventResponse]
)
def get_calendar_events(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    events = []

    # =====================
    # 1️⃣ Loans visibles
    # =====================
    loans_query = db.query(Loan)

    if not current_user.has_permission("loan:view_all"):
        loans_query = loans_query.filter(Loan.user_id == current_user.id)

    loans = loans_query.all()

    for loan in loans:
        events.append({
            "id": loan.id,
            "title": f"Retour : {loan.book.title}",
            "start": loan.due_date,
            "end": loan.due_date,
            "level": "danger" if loan.status in ["late"] else "warning",
            "type": "loan"
        })

    # =====================
    # 2️⃣ Events perso
    # =====================
    personal_events = db.query(CalendarEvent).filter(
        CalendarEvent.user_id == current_user.id
    ).all()

    for ev in personal_events:
        events.append({
            "id": ev.id,
            "title": ev.title,
            "start": ev.start_date,
            "end": ev.end_date,
            "level": ev.level,
            "type": ev.type
        })

    return events

@router.get("/events", response_model=list[CalendarEventResponse])
def list_events(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    events = crud.get_events(db, current_user.id)
    return [
        {
            "id": e.id,
            "title": e.title,
            "start": e.start_date,
            "end": e.end_date,
            "level": e.level,
            "type": e.type
        }
        for e in events
    ]


@router.put("/events/{event_id}", response_model=CalendarEventResponse)
def update_event(
    event_id: int,
    data: CalendarEventUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    e = crud.update_event(db, event_id, data, current_user.id)
    return {
        "id": e.id,
        "title": e.title,
        "start": e.start_date,
        "end": e.end_date,
        "level": e.level,
        "type": e.type
    }

@router.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    crud.delete_event(db, event_id, current_user.id)
    return {"detail": "Event deleted"}
