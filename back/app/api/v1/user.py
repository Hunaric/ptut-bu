from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import user as crud_user
from app.schemas.user import User, UserCreate
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.create_user(db, user_in)
    return db_user
