from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.book import BookFilter
from app.schemas.loan import LoanFilter
from app.crud.loan import query_loans
from app.crud.book import query_books
router = APIRouter(prefix="/query", tags=["Dynamic Queries"])

@router.post("/books")
def dynamic_books_query(filters: BookFilter, db: Session = Depends(get_db)):
    return query_books(db, filters)

@router.post("/loans")
def dynamic_loans_query(filters: LoanFilter, db: Session = Depends(get_db)):
    return query_loans(db, filters) 