from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from typing import List, Optional
from app.models.user import User as UserModel

from app.core.dependencies import require_permission
from app.core.database import get_db
from app.schemas.user import UserCreate, User, UserUpdate
from app.schemas.account import AccountUpdate
from app.crud.user import create_user_with_account, update_user, get_user, assign_permission_to_user, remove_permission_from_user, get_user_by_identifier, get_user_by_email
from app.crud.account import update_account

router = APIRouter(prefix="/users", tags=["Users"])

# CREATE User + Account
# @router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_with_account(db, user)
    

# GET all users
@router.get("/", response_model=List[User])
def list_users(
    skip: int = Query(0, ge=0, description="Nombre d'utilisateurs à sauter"),
    limit: int = Query(50, le=200, description="Nombre maximum d'utilisateurs à retourner"),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des utilisateurs.
    Paramètres:
    - skip: nombre d'utilisateurs à sauter (pagination)
    - limit: nombre maximum d'utilisateurs à retourner
    """
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users


# UPDATE User + Account
@router.put("/{user_id}", response_model=User)
def update_user_info(user_id: str, updates: UserUpdate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(404, "User not found")

    return update_user(db, db_user, updates)

# UPDATE Account linked to User
@router.put("/{user_id}/account", response_model=User) 
def update_account_info(user_id: str, updates: AccountUpdate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(404, "User not found")

    if not db_user.account:
        raise HTTPException(404, "Account not found")

    updated_account = update_account(db, db_user.account, updates)
    return db_user


@router.post("/{user_id}/permissions/{permission_id}", response_model=User, dependencies=[Depends(require_permission("loan:manage"))])
def add_permission_to_user(user_id: str, permission_id: int, db: Session = Depends(get_db)):
    user = assign_permission_to_user(db, user_id, permission_id)
    return user


@router.delete("/{user_id}/permissions/{permission_id}", response_model=User, dependencies=[Depends(require_permission("loan:manage"))])
def remove_permission_from_user_endpoint(user_id: str, permission_id: int, db: Session = Depends(get_db)):
    user = remove_permission_from_user(db, user_id, permission_id)
    return user


@router.get("/by-identifier/{identifier}", response_model=User)
def get_unique_user(identifier: str, db: Session = Depends(get_db)):
    user = get_user_by_identifier(db, identifier)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.get("/mail/{email}", response_model=User, deprecated=True, description="This endpoint is deprecated. Use /users/{identifier} instead.")
def get_user_by_email_endpoint(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(404, "User not found")
    return user