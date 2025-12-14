from app.models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import book as crud
from app.schemas.book import Book, BookCreate
from app.core.dependencies import require_admin, require_superuser
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=list[Book])
def list_books(db: Session = Depends(get_db)):
    return crud.get_books(db)

@router.post("/", response_model=Book)
def add_book(book: BookCreate, db: Session = Depends(get_db), 
    current_user: User = Depends(require_admin)
):
    return crud.create_book(db, book)

# Accessible uniquement aux superusers
@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_superuser)
):
    return crud.delete_book(db, book_id)