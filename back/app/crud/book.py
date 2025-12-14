from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate

def get_books(db: Session):
    return db.query(Book).all()

def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.loans and any(loan.status == "ongoing" for loan in book.loans):
        raise HTTPException(
            status_code=400,
            detail="Cannot delete a book currently on loan."
        )

    db.delete(book)
    db.commit()
    return {"detail": "Book deleted successfully"}
