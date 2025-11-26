from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email_etablissement: EmailStr
    username: str
    role_id: Optional[int] = None   # rend le champ optionnel
    person_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

    model_config = {
        "from_attributes": True
    }

class User(UserBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

