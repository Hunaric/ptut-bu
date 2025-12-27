import uuid
from app.schemas.pagination import PaginatedResponse
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.crud import loan as crud
from app.schemas.loan import LoanCreate, LoanResponse, LoanFilter, LoanUpdateStatus
from app.core.dependencies import require_admin, require_permission, require_superuser, get_current_user, require_any_permission
from app.core.database import get_db
from app.models.user import User
from datetime import date
from app.models.loan import Loan

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post(
    "/",
    response_model=LoanResponse,
    dependencies=[Depends(require_any_permission("loan:create", "loan:manage"))]
)
def create_loan_route(
    data: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # <-- récupère l'utilisateur connecté
):
    # Utiliser current_user.id comme user_id
    return crud.create_loan(db, data, current_user.id)



@router.get("/late")
def get_late_loans(db: Session = Depends(get_db)):
    today = date.today()
    loans = db.query(Loan).filter(
        Loan.return_date.is_(None),
        Loan.due_date < today
    ).all()

    return [
        {
            "id": loan.id,
            "book_title": loan.book.title,
            "due_date": loan.due_date.isoformat(),
            "borrower_name": getattr(loan.borrower, "name", None)
        }
        for loan in loans
    ]

@router.get("/{loan_id}", response_model=LoanResponse)
def read_loan(loan_id: int, db: Session = Depends(get_db)):
    return crud.get_loan_by_id(db, loan_id)

@router.get("/", response_model=list[LoanResponse])
def read_all_loans(db: Session = Depends(get_db)):
    return crud.get_all_loans(db)

@router.get(
    "/advanced",
    response_model=PaginatedResponse[LoanResponse],
    dependencies=[Depends(require_any_permission("loan:view_all", "loan:admin"))]
)
def read_loans_advanced(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_loans_advanced(db, page, size)

@router.get(
    "/user/{user_id}",
    response_model=list[LoanResponse],
    dependencies=[Depends(require_any_permission("loan:view", "loan:admin"))]
)
def read_user_loans(
    user_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    return crud.get_user_loans(db, user_id)

@router.post(
    "/{loan_id}/approve",
    response_model=LoanResponse,
    dependencies=[Depends(require_permission("loan:manage"))]
)
def approve_loan_route(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.approve_loan(db, loan_id, current_user)


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



@router.patch(
    "/{loan_id}/status",
    response_model=LoanResponse,
    dependencies=[Depends(require_permission("loan:manage"))]
)
def update_loan_status(
    loan_id: int,
    update: LoanUpdateStatus,
    db: Session = Depends(get_db)
):
    return crud.update_loan_status(db, loan_id, update.status)

