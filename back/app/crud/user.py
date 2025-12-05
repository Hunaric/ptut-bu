from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud.account import create_account
from app.core.security import hash_password  # si tu utilises fastapi security

def create_user_with_account(db: Session, user: UserCreate):
    # 1. Création du compte
    db_account = create_account(db, user.account)

    # 2. Création du user lié
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.hashed_password),
        account_id=db_account.id,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def update_user(db: Session, db_user: User, updates: UserUpdate):
    if updates.password:
        db_user.hashed_password = hash_password(updates.password)

    for key, value in updates.dict(exclude_unset=True, exclude={"password"}).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()