from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.core.database import get_db
from app.models.book import Book
from app.models.loan import Loan
from datetime import date

router = APIRouter()

@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):

    # 1️⃣ Nombre de livres par catégorie
    books_per_category = (
        db.query(Book.category_id, func.count(Book.id))
        .group_by(Book.category_id)
        .all()
    )
    books_per_category = [
        {"category_id": c, "count": count} for c, count in books_per_category
    ]

    # 2️⃣ Nombre de prêts par mois (2020-2025)
    loans_per_month = (
        db.query(
            extract('year', Loan.loan_date).label('year'),
            extract('month', Loan.loan_date).label('month'),
            func.count(Loan.id)
        )
        .filter(Loan.loan_date >= date(2020, 1, 1))
        .filter(Loan.loan_date <= date(2025, 12, 31))
        .group_by('year', 'month')
        .order_by('year', 'month')
        .all()
    )
    loans_per_month = [
        {"year": int(y), "month": int(m), "count": count} 
        for y, m, count in loans_per_month
    ]

    # 3️⃣ Taux de retour à temps vs en retard
    total_loans = db.query(func.count(Loan.id)).scalar()
    on_time = (
        db.query(func.count(Loan.id))
        .filter(Loan.return_date != None)
        .filter(Loan.return_date <= Loan.due_date)
        .scalar()
    )
    late = total_loans - on_time

    return {
        "books_per_category": books_per_category,
        "loans_per_month": loans_per_month,
        "loan_return_stats": {
            "total": total_loans,
            "on_time": on_time,
            "late": late
        }
    }
