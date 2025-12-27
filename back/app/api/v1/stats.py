from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.core.database import get_db
from app.models.book import Book
from app.models.loan import Loan
from datetime import date


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

@router.get("/dashboard")
def dashboard_stats(year: int = date.today().year, db: Session = Depends(get_db)):
    return {
        "loans_by_month": loans_by_month(db, year),
        "on_time_return_rate": on_time_return_rate_global(db),
        "metrics": metrics(db, year)
    }
