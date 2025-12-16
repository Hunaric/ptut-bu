from app.models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import book as crud
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.core.dependencies import require_admin, require_superuser
from app.core.database import get_db

router = APIRouter()

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookResponse)
def create(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

@router.get("/", response_model=list[BookResponse])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip, limit)

@router.get("/{book_id}", response_model=BookResponse)
def read_one(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book(db, book_id)

@router.put("/{book_id}", response_model=BookResponse)
def update(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    return crud.update_book(db, book_id, book)

@router.delete("/{book_id}")
def delete(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(db, book_id)
