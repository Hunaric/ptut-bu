# app/api/v1/auth.py
from app.core.auth import create_access_token
from app.core.database import get_db
from app.crud.user import get_user_by_email

from passlib.context import CryptContext
from app.schemas.auth import LoginRequest, TokenResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/user/login", response_model=TokenResponse)
def user_login(login_in: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, login_in.email)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not pwd_context.verify(login_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # sub = id du client
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

