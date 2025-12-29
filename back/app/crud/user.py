from operator import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud.account import create_account
from app.core.security import hash_password
from app.models.permission import Permission 

def create_user_with_account(db: Session, user: UserCreate):
    # 1. Création du compte
    db_account = create_account(db, user.account)

    # 2. Création du user lié
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.hashed_password),
        account_id=db_account.id,
        role_id=user.role_id
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


def get_user_by_identifier(db: Session, identifier: str):
    return (
        db.query(User)
        .filter(
            or_(
                User.email == identifier,
                User.username == identifier
            )
        )
        .first()
    )


def assign_permission_to_user(db: Session, user_id: str, permission_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    permission = db.query(Permission).filter(Permission.id == permission_id).first()

    if not user or not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or Permission not found"
        )

    if permission in user.permissions:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission already assigned to this user"
        )

    user.permissions.append(permission)
    db.commit()
    db.refresh(user)

    return user


def remove_permission_from_user(db: Session, user_id: str, permission_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    permission = db.query(Permission).filter(Permission.id == permission_id).first()

    if not user or not permission:
        raise HTTPException(status_code=404, detail="User or Permission not found")

    if permission in user.permissions:
        user.permissions.remove(permission)
        db.commit()
        db.refresh(user)

    return user
