from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from typing import Optional
from sqlalchemy import or_
from typing import List
from app.models.book import Book
from app.models.tag import Tag
from app.schemas.book import BookCreate, BookFilter, BookUpdate
from app.schemas.pagination import PaginatedResponse
from app.schemas.book import BookResponse   


def get_books(db: Session):
    return db.query(Book).all()

def create_book(db: Session, book: BookCreate):
    if book.isbn:
        existing = db.query(Book).filter(Book.isbn == book.isbn).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="ISBN already exists"
            )

    # On exclut les tags ET cover_url pour éviter les doublons
    book_data = book.dict(exclude={"tags", "cover_url"})
    # On calcule cover_url à partir de l'ISBN
    book_data["cover_url"] = get_cover_url(book.isbn)

    db_book = Book(**book_data)

    if book.tags:
        tags = db.query(Tag).filter(Tag.id.in_(book.tags)).all()
        db_book.tags = tags

    try:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid data (foreign key or constraint error)"
        )


def update_book(db: Session, book_id: int, book_data: BookUpdate):
    book = get_book(db, book_id)

    data = book_data.dict(exclude_unset=True, exclude={"tags"})

    if "isbn" in data:
        data["cover_url"] = get_cover_url(data["isbn"])

    for key, value in data.items():
        setattr(book, key, value)

    if book_data.tags is not None:
        tags = db.query(Tag).filter(Tag.id.in_(book_data.tags)).all()
        book.tags = tags

    try:
        db.commit()
        db.refresh(book)
        return book

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="ISBN already exists"
        )



def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()

def get_books_advanced(
    db: Session,
    page: int = 1,
    size: int = 10,
    category_id: Optional[int] = None,
    tag_ids: Optional[List[int]] = None
):
    query = db.query(Book)

    if category_id:
        query = query.filter(Book.category_id == category_id)

    if tag_ids:
        query = (
            query.join(Book.tags)
            .filter(Tag.id.in_(tag_ids))
            .group_by(Book.id)
            .having(func.count(Tag.id) == len(tag_ids))
        )

    total = query.count()

    books = (
        query
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return PaginatedResponse[BookResponse](
        total=total,
        page=page,
        size=size,
        items=[BookResponse.from_orm(b) for b in books]
    )


def get_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()

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


def query_books(db: Session, filters: BookFilter):
    query = db.query(Book)

    if filters.title:
        query = query.filter(Book.title.ilike(f"%{filters.title}%"))
    if filters.author:
        query = query.filter(Book.author.ilike(f"%{filters.author}%"))
    if filters.published_after:
        query = query.filter(Book.published_year >= filters.published_after)
    if filters.published_before:
        query = query.filter(Book.published_year <= filters.published_before)
    if filters.category_ids:
        query = query.filter(Book.category_id.in_(filters.category_ids))
    if filters.tag_ids:
        query = query.join(Book.tags).filter(Tag.id.in_(filters.tag_ids))

    return query.all()

def get_cover_url(isbn: str | None) -> str | None:
    if not isbn:
        return None
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"


def search_books_by_title(db: Session, title: str):
    query = db.query(Book).filter(or_(
            Book.title.ilike(f"%{title}%"),
            Book.author.ilike(f"%{title}%")
        )
        )
    return query.all()