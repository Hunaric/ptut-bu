# app/api/v1/auth.py
from app.core.auth import create_access_token
from app.core.database import get_db
from app.crud.user import get_user_by_identifier

from passlib.context import CryptContext
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.account import AccountCreate, RegisterRequest
from app.api.v1.user import create_user
from app.crud.account import create_account
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
router = APIRouter()

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=TokenResponse)
def user_login(login_in: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_identifier(db, login_in.identifier)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not pwd_context.verify(login_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email/username or password")

    # sub = id du client
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=TokenResponse)
def register_user(reg_in: RegisterRequest, db: Session = Depends(get_db)):
    # Transformer RegisterRequest en AccountCreate
    account_data = AccountCreate(
        nom=reg_in.nom,
        prenom=reg_in.prenom,
        sexe=reg_in.sexe,
        etablissement=reg_in.etablissement,
        numero=reg_in.numero,
        rue=reg_in.rue,
        boite_postale=reg_in.boite_postale,
        code_postal=reg_in.code_postal,
        ville=reg_in.ville,
        codex_ville=reg_in.codex_ville,
        pays=reg_in.pays,
        telephone=reg_in.telephone,
        email=reg_in.email,
        password=reg_in.password, 
        username=reg_in.username
    )
    
    try:
        account = create_account(db, account_data)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    # user = create_user(db, reg_in)
    access_token = create_access_token(data={"sub": str(account.user.id)})
    # return {"access_token": access_token, "token_type": "bearer"}
    
    return {
    "access_token": access_token,
    "token_type": "bearer"
    }
