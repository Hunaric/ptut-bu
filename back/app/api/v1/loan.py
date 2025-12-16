from app.models.user import User
from app.schemas.pagination import PaginatedResponse
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud import loan as crud
from app.schemas.loan import LoanCreate, LoanResponse, LoanFilter
from app.core.dependencies import require_admin, require_permission, require_superuser, get_current_user, require_any_permission
from app.core.database import get_db

router = APIRouter()

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post(
    "/",
    response_model=LoanResponse,
    dependencies=[Depends(require_any_permission("loan:create", "loan:manage"))]
)
def create_loan_route(
    data: LoanCreate,
    db: Session = Depends(get_db)
):
    return crud.create_loan(db, data)

@router.post(
    "/{loan_id}/return",
    response_model=LoanResponse,
    dependencies=[Depends(require_permission("loan:return"))]
)
def return_loan_route(
    loan_id: int,
    db: Session = Depends(get_db)
):
    return crud.return_loan(db, loan_id)

@router.post(
    "/search",
    response_model=list[LoanResponse],
    dependencies=[Depends(require_any_permission("loan:view_all", "loan:admin"))]
)
def search_loans(
    filters: LoanFilter,
    db: Session = Depends(get_db)
):
    return crud.query_loans(db, filters)

