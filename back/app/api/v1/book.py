from app.models.user import User
from app.schemas.pagination import PaginatedResponse
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud import book as crud
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.core.dependencies import require_admin, require_permission, require_superuser
from app.core.database import get_db

router = APIRouter()

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookResponse)
def create(book: BookCreate, db: Session = Depends(get_db),
        #    current_user: User = Depends(require_admin)
           ):
    return crud.create_book(db, book)

@router.get("/", response_model=list[BookResponse])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip, limit)

@router.get(
    "/advanced",
    response_model=PaginatedResponse[BookResponse]
)
def read_books_advanced(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = None,
    tag_ids: Optional[List[int]] = Query(None),
    db: Session = Depends(get_db)
):
    return crud.get_books_advanced(
        db=db,
        page=page,
        size=size,
        category_id=category_id,
        tag_ids=tag_ids
    )

@router.get("/{book_id}", response_model=BookResponse)
def read_one(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book(db, book_id)

@router.put("/{book_id}", response_model=BookResponse)
def update(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    return crud.update_book(db, book_id, book)

@router.delete(
    "/{book_id}",
    dependencies=[Depends(require_permission("book:delete"))]
    )
def delete(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(db, book_id)

# L'utilisateur doit avoir la permission "loan:create" et "loan:validate" pour emprunter un livre (les deux sont requises)
# dependencies=[
#     Depends(require_permission("loan:create")),
#     Depends(require_permission("loan:validate"))
# ]
