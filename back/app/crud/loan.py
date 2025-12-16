from datetime import date
from sqlalchemy.orm import Session
from app.models.loan import Loan
from app.schemas.loan import LoanCreate, LoanFilter
from fastapi import HTTPException

def create_loan(db: Session, data: LoanCreate):
    loan = Loan(
        book_id=data.book_id,
        user_id=data.user_id,
        loan_date=date.today(),
        due_date=data.due_date,
        status="ongoing"
    )

    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def return_loan(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if not loan:
        raise HTTPException(404, "Loan not found")

    if loan.status == "returned":
        raise HTTPException(400, "Loan already returned")

    loan.return_date = date.today()

    if loan.return_date > loan.due_date:
        loan.status = "late"
    else:
        loan.status = "returned"

    db.commit()
    db.refresh(loan)
    return loan


def query_loans(db: Session, filters: LoanFilter):
    query = db.query(Loan)

    if filters.student_ids:
        query = query.filter(Loan.user_id.in_(filters.student_ids))

    if filters.status:
        query = query.filter(Loan.status == filters.status)

    if filters.overdue:
        query = query.filter(
            Loan.status == "ongoing",
            Loan.due_date < date.today()
        )

    return query.all()
