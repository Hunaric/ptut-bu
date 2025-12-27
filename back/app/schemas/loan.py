from typing import Literal
from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from uuid import UUID
from enum import Enum

class LoanStatus(str, Enum):
    requested = "requested"
    approved = "approved"
    ongoing = "ongoing"
    returned = "returned"
    late = "late"


# --------------------------
# Input pour créer un prêt
# --------------------------
class LoanCreate(BaseModel):
    book_id: int
    # plus besoin de user_id ici, il sera pris depuis le token JWT

# --------------------------
# Input pour retourner un livre
# --------------------------
class LoanReturn(BaseModel):
    return_date: Optional[date] = None

# --------------------------
# Input pour mettre à jour un prêt (ex: prolongation)
# --------------------------
class LoanUpdate(BaseModel):
    due_date: Optional[date] = None

# --------------------------
# Réponse d'un prêt
# --------------------------
class LoanResponse(BaseModel):
    id: int
    book_id: int
    user_id: Optional[UUID]
    loan_date: Optional[date]
    due_date: Optional[date]
    return_date: Optional[date]
    status: str
    ticket: Optional[str]
    book_quantity: Optional[int]  # quantité actuelle du livre

    model_config = {
        "from_attributes": True
    }

# --------------------------
# Filtres pour rechercher des prêts
# --------------------------
class LoanFilter(BaseModel):
    student_ids: Optional[List[UUID]] = None
    status: Optional[str] = None      # ongoing, returned, late
    overdue: Optional[bool] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None



class LoanUpdateStatus(BaseModel):
    status: LoanStatus