from app.models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import category as crud
from app.schemas.category import Category, CategoryBase
from app.core.dependencies import require_admin, require_superuser
from app.core.database import get_db

router = APIRouter()

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[Category])
def list_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@router.post("/", response_model=CategoryBase)
def add_category(category: CategoryBase, db: Session = Depends(get_db), 
    # current_user: User = Depends(require_admin)
):
    return crud.create_category(db, category)

# Accessible uniquement aux superusers
@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_superuser)
):
    return crud.delete_category(db, category_id)