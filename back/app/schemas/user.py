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

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None

class User(UserBase):
    id: int
    account: Optional[Account] = None

    class Config:
        from_attributes = True
        