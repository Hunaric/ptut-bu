# app/api/v1/auth.py
from app.core.auth import create_access_token
from app.core.database import get_db
from app.core.dependencies import get_current_user
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

    
@router.get("/me")
def get_me(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Récupérer le rôle (s'il existe)
    role = current_user.role

    # Récupérer les permissions provenant du rôle
    role_permissions = {perm.name for perm in role.permissions} if role else set()

    # Récupérer les permissions directes de l'utilisateur
    user_permissions = {perm.name for perm in current_user.permissions}

    # Fusionner toutes les permissions
    all_permissions = role_permissions | user_permissions

    # Si superuser, on peut ajouter un flag ou toutes les permissions
    if current_user.is_superuser:
        all_permissions.add("superuser")  # ou mettre un flag spécifique

    return {
        # "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": role.name if role else None,
        "permissions": list(all_permissions)
    }




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
