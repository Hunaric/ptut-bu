from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.core.database import get_db
from app.models.book import Book
from app.models.loan import Loan
from datetime import date
from app.crud.loan import get_user_loans
from app.core.dependencies import require_admin, require_permission, require_superuser, get_current_user, require_any_permission


router = APIRouter(prefix="/stats", tags=["Stats"])

# @router.get("/dashboard/stats")
# def get_dashboard_stats(db: Session = Depends(get_db)):

#     loans_per_month = (
#         db.query(
#             extract('month', Loan.loan_date).label('month'),
#             func.count(Loan.id).label('count')
#         )
#         .filter(Loan.loan_date >= date(2025, 1, 1))
#         .group_by('month')
#         .order_by('month')
#         .all()
#     )

#     return {
#         "loans_per_month": [
#             {"month": int(m), "count": count}
#             for m, count in loans_per_month
#         ]
#     }

def loans_by_month(db: Session, year: int):
    results = (
        db.query(
            extract("month", Loan.loan_date).label("month"),
            func.count(Loan.id)
        )
        .filter(extract("year", Loan.loan_date) == year)
        .group_by("month")
        .order_by("month")
        .all()
    )

    # tableau de 12 mois (index 0 = Janvier)
    data = [0] * 12
    for month, count in results:
        data[int(month) - 1] = count

    return data

def on_time_return_rate_global(db: Session):
    total_returns = db.query(func.count(Loan.id)) \
        .filter(Loan.return_date.isnot(None)) \
        .scalar()

    if total_returns == 0:
        return 0

    on_time = db.query(func.count(Loan.id)) \
        .filter(
            Loan.return_date.isnot(None),
            Loan.return_date <= Loan.due_date
        ).scalar()

    return round((on_time / total_returns) * 100, 2)

def on_time_return_rate_by_year(db: Session, year: int):
    total_returns = db.query(func.count(Loan.id)) \
        .filter(
            extract("year", Loan.loan_date) == year,
            Loan.return_date.isnot(None)
        ).scalar()

    if total_returns == 0:
        return 0

    on_time = db.query(func.count(Loan.id)) \
        .filter(
            extract("year", Loan.loan_date) == year,
            Loan.return_date.isnot(None),
            Loan.return_date <= Loan.due_date
        ).scalar()

    return round((on_time / total_returns) * 100, 2)

def user_dashboard_stats(user_id: int, db: Session, year: int = date.today().year):
    loans = [
        loan for loan in get_user_loans(db, user_id)
        if loan.loan_date.year == year
    ]

    total_loans = len(loans)

    if total_loans == 0:
        return {
            "scope": "user",
            "loans_by_month": [0] * 12,
            "on_time_return_rate": 0,
            "metrics": {
                "total_books": db.query(func.count(Book.id)).scalar(),
                "total_loans": 0,
                "active_loans": 0,
                "late_loans": 0,
                "return_rate": 0,
            },
        }

    # loans par mois
    loans_by_month = [0] * 12
    for loan in loans:
        loans_by_month[loan.loan_date.month - 1] += 1

    on_time_returns = sum(
        1 for loan in loans
        if loan.return_date and loan.return_date <= loan.due_date
    )

    active_loans = sum(1 for loan in loans if loan.return_date is None)
    late_loans = sum(
        1 for loan in loans
        if loan.return_date is None and loan.due_date < date.today()
    )

    on_time_rate = round((on_time_returns / total_loans) * 100, 2)

    return {
        "scope": "user",
        "loans_by_month": loans_by_month,
        "on_time_return_rate": on_time_rate,
        "metrics": {
            "total_books": db.query(func.count(Book.id)).scalar(),
            "total_loans": total_loans,
            "active_loans": active_loans,
            "late_loans": late_loans,
            "return_rate": on_time_rate,
        },
    }

def metrics(db: Session, year: int):
    today = date.today()

    # Filtrer les loans sur l'année
    total_loans = db.query(func.count(Loan.id)) \
        .filter(extract("year", Loan.loan_date) == year) \
        .scalar()

    active_loans = db.query(func.count(Loan.id)) \
        .filter(
            extract("year", Loan.loan_date) == year,
            Loan.return_date.is_(None)
        ).scalar()

    late_loans = db.query(func.count(Loan.id)) \
        .filter(
            extract("year", Loan.loan_date) == year,
            Loan.return_date.is_(None),
            Loan.due_date < today
        ).scalar()

    return {
        "total_books": db.query(func.count(Book.id)).scalar(),  # livres totaux restent globaux
        "total_loans": total_loans,
        "active_loans": active_loans,
        "late_loans": late_loans,
        "return_rate": on_time_return_rate_by_year(db, year)
    }

@router.get(
    "/dashboard",
    dependencies=[Depends(require_any_permission("loan:manage", "loan:view_all"))]
)
def dashboard_stats(year: int = date.today().year, db: Session = Depends(get_db)):
    return {
        "scope": "global",
        "loans_by_month": loans_by_month(db, year),
        "on_time_return_rate": on_time_return_rate_global(db),
        "metrics": metrics(db, year)
    }

@router.get("/user/{user_id}/loans", dependencies=[Depends(require_any_permission("loan:view_own", "loan:view_all"))])
def user_loan_stats(user_id: int, db: Session = Depends(get_db)):
    loans = get_user_loans(db, user_id)
    total_loans = len(loans)
    if total_loans == 0:
        return {
            "total_loans": 0,
            "on_time_return_rate": 0,
            "metrics": {
                "total_books": db.query(func.count(Book.id)).scalar(),
                "total_loans": 0,
                "active_loans": 0,
                "late_loans": 0,
                "return_rate": 0
            }
        }

    on_time_returns = sum(1 for loan in loans if loan.return_date and loan.return_date <= loan.due_date)

    return {
        "total_loans": total_loans,
        "on_time_return_rate": round((on_time_returns / total_loans) * 100, 2),
        "metrics": {
            "total_books": db.query(func.count(Book.id)).scalar(),
            "total_loans": total_loans,
            "active_loans": sum(1 for loan in loans if loan.return_date is None),
            "late_loans": sum(1 for loan in loans if loan.return_date is None and loan.due_date < date.today()),
            "return_rate": round((on_time_returns / total_loans) * 100, 2)
        }
    }

@router.get("/user/dashboard")
def user_dashboard(
    year: int = date.today().year,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user is None:
        return {"detail": "Authentication required."}

    if current_user.has_permission("loan:manage", "loan:view_all"):
        return dashboard_stats(year=year, db=db)

    return user_dashboard_stats(current_user.id, db, year)
