from app.schemas.role import RoleResponse
from pydantic import BaseModel
from typing import Optional
from .account import Account, AccountCreate

class UserBase(BaseModel):
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    account: AccountCreate
    role_id: Optional[int] = None

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None
    role: Optional[RoleResponse] = None

class User(UserBase):
    id: int
    role: Optional[RoleResponse] = None
    account: Optional[Account] = None

    model_config = {
        "from_attributes": True
    }
