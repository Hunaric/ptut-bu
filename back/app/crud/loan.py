from datetime import date, timedelta
from app.schemas.pagination import PaginatedResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.loan import Loan
from app.models.user import User
from app.models.book import Book
from app.schemas.loan import LoanCreate, LoanFilter, LoanStatus
import uuid
from datetime import date, timedelta

def get_loan_by_id(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(404, "Loan not found")
    return loan

def get_all_loans(db: Session):
    return db.query(Loan).all()

def get_loans_advanced(
    db: Session,
    page: int = 1,
    size: int = 10
):
    query = db.query(Loan)

    total = query.count()

    loans = (
        query
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return PaginatedResponse[Loan](
        total=total,
        page=page,
        size=size,
        items=loans
    )

def create_loan(db: Session, data: LoanCreate, user_id: uuid.UUID):
    book = db.query(Book).filter(Book.id == data.book_id).first()
    if not book:
        raise HTTPException(404, "Book not found")

    if book.quantity <= 0:
        raise HTTPException(400, "No copies available")

    loan = Loan(
        book_id=book.id,
        user_id=user_id,
        ticket=str(uuid.uuid4()),
        loan_date=date.today(),
        due_date=date.today() + timedelta(days=14)
    )

    # Mettre à jour la quantité de copies disponibles
    book.quantity -= 1

    # Ajouter la quantité actuelle au prêt
    loan.book_quantity = book.quantity

    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def approve_loan(db: Session, loan_id: int, staff_user: User):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if loan.status != "requested":
        raise HTTPException(400, "Loan cannot be approved")

    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if book.quantity <= 0:
        raise HTTPException(400, "No copies available")

    book.quantity -= 1

    loan.status = "approved"
    loan.loan_date = date.today()
    loan.due_date = date.today() + timedelta(days=14)

    # 👇 ICI
    loan.approved_by_id = staff_user.id

    db.commit()
    db.refresh(loan)
    return loan


def return_loan(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(404, "Loan not found")

    if loan.status not in ["approved", "ongoing"]:
        raise HTTPException(400, "Loan cannot be returned")

    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if not book:
        raise HTTPException(404, "Book not found")

    book.quantity += 1
    loan.return_date = date.today()
    loan.status = "returned" if loan.return_date <= loan.due_date else "late"
    db.commit()
    db.refresh(loan)

    loan.book_quantity = book.quantity
    return loan

def update_loan_status(db: Session, loan_id: int, new_status: LoanStatus):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(404, "Loan not found")

    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if not book:
        raise HTTPException(404, "Book not found")

    # logique selon le nouveau status
    if new_status == LoanStatus.approved:
        if book.quantity <= 0:
            raise HTTPException(400, "No copies available for this book")
        book.quantity -= 1
        loan.loan_date = date.today()
        loan.due_date = date.today() + timedelta(days=14)
    elif new_status in [LoanStatus.returned, LoanStatus.late]:
        book.quantity += 1
        loan.return_date = date.today()

    loan.status = new_status
    loan.book_quantity = book.quantity

    db.commit()
    db.refresh(loan)
    return loan

def get_user_loans(db: Session, user_id: uuid.UUID):
    return db.query(Loan).filter(Loan.user_id == user_id).all()