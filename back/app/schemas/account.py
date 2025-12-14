from pydantic import BaseModel
from typing import Optional
import uuid

class AccountBase(BaseModel):
    sexe: str
    nom: str
    prenom: str
    etablissement: str

    numero: Optional[str] = None
    rue: Optional[str] = None
    boite_postale: Optional[str] = None
    code_postal: Optional[str] = None
    ville: Optional[str] = None
    codex_ville: Optional[str] = None
    pays: Optional[str] = None
    telephone: Optional[str] = None

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    pass

class Account(AccountBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
