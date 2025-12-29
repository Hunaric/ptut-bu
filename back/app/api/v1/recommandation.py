from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.core.database import get_db
from app.schemas.book import RecommendedBook
from app.models.book import Book
from app.models.loan import Loan
from datetime import date
from app.crud.loan import get_user_loans
from app.core.dependencies import (
    require_admin, require_permission, require_superuser,
    get_current_user, require_any_permission
)

router = APIRouter(prefix="/recommandation", tags=["Recommandation"])


# 1 - Récupérer les livres déjà empruntés par l’utilisateur
# 2 - Identifier les catégories / auteurs dominants
# 3 - Recommander d’autres livres non encore empruntés

def recommend_books_for_user(db: Session, user_id: int, limit: int = 10):

    favorite_categories = (
        db.query(Book.category_id)
        .join(Loan, Loan.book_id == Book.id)
        .filter(Loan.user_id == user_id)
        .group_by(Book.category_id)
        .order_by(func.count(Loan.id).desc())
        .limit(3)
        .subquery()
    )

    results = (
        db.query(
            Book,
            func.count(Loan.id).label("score")
        )
        .join(Loan, Loan.book_id == Book.id)
        .filter(
            Book.category_id.in_(favorite_categories),
            ~Book.id.in_(
                db.query(Loan.book_id)
                .filter(Loan.user_id == user_id)
            )
        )
        .group_by(Book.id)
        .order_by(func.count(Loan.id).desc())
        .limit(limit)
        .all()
    )

    # 🔥 Mapping explicite vers le schema
    return [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "description": book.description,
            "isbn": book.isbn,
            "published_year": book.published_year,
            "category_id": book.category_id,
            "quantity": book.quantity,
            "cover_url": book.cover_url
        }
        for book, score in results
    ]


def recommend_similar_books(db: Session, book_id: int, limit: int = 10):
    sub_users = (
        db.query(Loan.user_id)
        .filter(Loan.book_id == book_id)
        .subquery()
    )

    return (
        db.query(Book, func.count(Loan.id).label("score"))
        .join(Loan)
        .filter(
            Loan.user_id.in_(sub_users),
            Book.id != book_id
        )
        .group_by(Book.id)
        .order_by(func.count(Loan.id).desc())
        .limit(limit)
        .all()
    )

def popular_books(db: Session, limit=10):
    return (
        db.query(Book, func.count(Loan.id).label("count"))
        .join(Loan)
        .group_by(Book.id)
        .order_by(func.count(Loan.id).desc())
        .limit(limit)
        .all()
    )


@router.get(
    "/user",
    response_model=list[RecommendedBook]
)
def user_recommendations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return recommend_books_for_user(db, current_user.id)

@router.get(
    "/book/{book_id}",
    response_model=list[RecommendedBook]
)
def similar_books(
    book_id: int,
    db: Session = Depends(get_db)
):
    results = recommend_similar_books(db, book_id)

    return [book for book, _ in results]

@router.get(
    "/popular",
    response_model=list[RecommendedBook]
)
def popular_books_endpoint(db: Session = Depends(get_db)):
    results = popular_books(db)
    return [book for book, _ in results]
