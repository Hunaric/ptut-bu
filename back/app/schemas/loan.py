from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID

class LoanBase(BaseModel):
    book_id: int
    due_date: date

class LoanCreate(LoanBase):
    user_id: UUID  # l’étudiant à qui on prête

class LoanReturn(BaseModel):
    return_date: Optional[date] = None

class LoanUpdate(BaseModel):
    due_date: Optional[date] = None

class LoanResponse(BaseModel):
    id: int
    book_id: int
    user_id: UUID
    loan_date: date
    due_date: date
    return_date: Optional[date]
    status: str

    model_config = {
        "from_attributes": True
    }

from typing import List

class LoanFilter(BaseModel):
    student_ids: Optional[List[UUID]] = None
    status: Optional[str] = None      # ongoing, returned, late
    overdue: Optional[bool] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None