from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, User, UserUpdate
from app.schemas.account import AccountUpdate
from app.crud.user import create_user_with_account, update_user, get_user
from app.crud.account import update_account

router = APIRouter(prefix="/users", tags=["Users"])

# CREATE User + Account
# @router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_with_account(db, user)
    
# UPDATE User + Account
@router.put("/{user_id}", response_model=User)
def update_user_info(user_id: int, updates: UserUpdate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(404, "User not found")

    return update_user(db, db_user, updates)

# UPDATE Account linked to User
@router.put("/{user_id}/account", response_model=User) 
def update_account_info(user_id: int, updates: AccountUpdate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(404, "User not found")

    if not db_user.account:
        raise HTTPException(404, "Account not found")

    updated_account = update_account(db, db_user.account, updates)
    return db_user