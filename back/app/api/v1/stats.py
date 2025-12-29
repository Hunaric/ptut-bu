from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.core.database import get_db
from app.models.book import Book
from app.models.loan import Loan
from datetime import date
from app.crud.loan import get_user_loans
from app.core.dependencies import (
    require_admin, require_permission, require_superuser,
    get_current_user, require_any_permission
)

router = APIRouter(prefix="/stats", tags=["Stats"])


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
    data = [0] * 12
    for month, count in results:
        data[int(month) - 1] = count
    return data


def on_time_return_rate_global(db: Session):
    """Taux global sur tous les prêts retournés"""
    returned_loans = db.query(Loan).filter(Loan.return_date.isnot(None)).all()
    if not returned_loans:
        return 0
    on_time = sum(1 for loan in returned_loans if loan.return_date <= loan.due_date)
    return round((on_time / len(returned_loans)) * 100, 2)


def on_time_return_rate_by_year(db: Session, year: int):
    """Taux pour l'année, uniquement sur les prêts retournés cette année"""
    returned_loans = db.query(Loan) \
        .filter(
            extract("year", Loan.loan_date) == year,
            Loan.return_date.isnot(None)
        ).all()
    if not returned_loans:
        return 0
    on_time = sum(1 for loan in returned_loans if loan.return_date <= loan.due_date)
    return round((on_time / len(returned_loans)) * 100, 2)


def user_dashboard_stats(user_id: int, db: Session, year: int = date.today().year):
    all_loans = get_user_loans(db, user_id)
    loans_this_year = [loan for loan in all_loans if loan.loan_date.year == year]

    returned_loans_global = [loan for loan in all_loans if loan.return_date]
    total_returns_global = len(returned_loans_global)
    on_time_returns_global = sum(1 for loan in returned_loans_global if loan.return_date <= loan.due_date)
    on_time_rate_global = round((on_time_returns_global / total_returns_global) * 100, 2) if total_returns_global else 0

    if not loans_this_year:
        return {
            "scope": "user",
            "loans_by_month": [0] * 12,
            "late_by_month": [0] * 12,
            "on_time_return_rate": on_time_rate_global,
            "metrics": {
                "total_books": db.query(func.count(Book.id)).scalar(),
                "total_loans": 0,
                "active_loans": 0,
                "late_loans": 0,
                "return_rate": 0,
            },
        }

    loans_by_month_list = [0] * 12
    late_by_month_list = [0] * 12
    active_loans = 0
    late_loans = 0

    today = date.today()
    for loan in loans_this_year:
        month_idx = loan.loan_date.month - 1
        loans_by_month_list[month_idx] += 1

        if loan.return_date is None:
            if loan.due_date < today:
                late_loans += 1
                late_by_month_list[month_idx] += 1
            else:
                active_loans += 1

    returned_this_year = [loan for loan in loans_this_year if loan.return_date]
    return_rate_year = round(
        (sum(1 for loan in returned_this_year if loan.return_date <= loan.due_date) / len(returned_this_year)) * 100, 2
    ) if returned_this_year else 0

    return {
        "scope": "user",
        "loans_by_month": loans_by_month_list,
        "late_by_month": late_by_month_list,
        "on_time_return_rate": on_time_rate_global,
        "metrics": {
            "total_books": db.query(func.count(Book.id)).scalar(),
            "total_loans": len(loans_this_year),
            "active_loans": active_loans,
            "late_loans": late_loans,
            "return_rate": return_rate_year,
        },
    }


def metrics(db: Session, year: int):
    today = date.today()
    loans_this_year = db.query(Loan).filter(extract("year", Loan.loan_date) == year).all()

    loans_by_month_list = [0] * 12
    late_by_month_list = [0] * 12
    active_loans = 0
    late_loans = 0

    for loan in loans_this_year:
        month_idx = loan.loan_date.month - 1
        loans_by_month_list[month_idx] += 1

        if loan.return_date is None:
            if loan.due_date < today:
                late_loans += 1
                late_by_month_list[month_idx] += 1
            else:
                active_loans += 1

    returned_this_year = [loan for loan in loans_this_year if loan.return_date]
    return_rate = round(
        (sum(1 for loan in returned_this_year if loan.return_date <= loan.due_date) / len(returned_this_year)) * 100, 2
    ) if returned_this_year else 0

    return {
        "total_books": db.query(func.count(Book.id)).scalar(),
        "total_loans": len(loans_this_year),
        "active_loans": active_loans,
        "late_loans": late_loans,
        "return_rate": return_rate,
        "loans_by_month": loans_by_month_list,
        "late_by_month": late_by_month_list,
    }


@router.get("/dashboard", dependencies=[Depends(require_any_permission("loan:manage", "loan:view_all"))])
def dashboard_stats(year: int = date.today().year, db: Session = Depends(get_db)):
    return {
        "scope": "global",
        "metrics": metrics(db, year),
        "on_time_return_rate": on_time_return_rate_global(db),
    }


@router.get("/user/{user_id}/loans", dependencies=[Depends(require_any_permission("loan:view_own", "loan:view_all"))])
def user_loan_stats(user_id: int, db: Session = Depends(get_db)):
    loans = get_user_loans(db, user_id)
    if not loans:
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

    returned_loans = [loan for loan in loans if loan.return_date]
    on_time_returns = sum(1 for loan in returned_loans if loan.return_date <= loan.due_date)
    total_returns = len(returned_loans)
    on_time_rate = round((on_time_returns / total_returns) * 100, 2) if total_returns else 0

    active_loans = sum(1 for loan in loans if loan.return_date is None)
    late_loans = sum(1 for loan in loans if loan.return_date is None and loan.due_date < date.today())

    return {
        "total_loans": len(loans),
        "on_time_return_rate": on_time_rate,
        "metrics": {
            "total_books": db.query(func.count(Book.id)).scalar(),
            "total_loans": len(loans),
            "active_loans": active_loans,
            "late_loans": late_loans,
            "return_rate": on_time_rate,
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
