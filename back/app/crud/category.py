from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryBase

def get_categories(db: Session):
    return db.query(Category).all()

def create_category(db: Session, category: CategoryBase):
    existing_category = db.query(Category).filter(Category.name == category.name).first()

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.books and any(book.loans and any(loan.status == "ongoing" for loan in book.loans) for book in category.books):
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category of book currently on loan."
        )

    db.delete(category)
    db.commit()
    return {"detail": "Category deleted successfully"}
