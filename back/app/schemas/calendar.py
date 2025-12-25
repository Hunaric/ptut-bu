# app/schemas/calendar.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

# =========================
# CREATE
# =========================
class CalendarEventCreate(BaseModel):
    title: str
    start_date: date
    end_date: Optional[date] = None
    level: str = "primary"

# =========================
# UPDATE
# =========================
class CalendarEventUpdate(BaseModel):
    title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    level: Optional[str] = None

# =========================
# RESPONSE (FullCalendar)
# =========================
class CalendarEventResponse(BaseModel):
    id: int
    title: str
    start: date
    end: Optional[date]
    level: str
    type: str

    model_config = {"from_attributes": True}
