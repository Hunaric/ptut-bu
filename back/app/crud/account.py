from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.account import Account
from app.models.user import User
from app.schemas.account import AccountCreate, AccountUpdate
from app.core.security import hash_password

# def create_account(db: Session, account: AccountCreate):
#     db_account = Account(**account.dict())
#     db.add(db_account)
#     db.commit()
#     db.refresh(db_account)
#     return db_account

def update_account(db: Session, db_account: Account, updates: AccountUpdate):
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_account, key, value)
    db.commit()
    db.refresh(db_account)
    return db_account


def create_account(db: Session, account_data: AccountCreate):
    # Vérification si nom + prénom existent déjà
    existing = db.query(Account).filter(
        Account.prenom == account_data.prenom,
        Account.nom == account_data.nom
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Un compte avec ce nom et prénom existe déjà.")

    # Créer l'Account
    account = Account(
        nom=account_data.nom,
        prenom=account_data.prenom,
        sexe=account_data.sexe,
        etablissement=account_data.etablissement,
        numero=account_data.numero,
        rue=account_data.rue,
        boite_postale=account_data.boite_postale,
        code_postal=account_data.code_postal,
        ville=account_data.ville,
        codex_ville=account_data.codex_ville,
        pays=account_data.pays,
        telephone=account_data.telephone
    )

    db.add(account)
    try:
        db.commit()
        db.refresh(account)  # 🟢 refresh pour obtenir l'ID
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erreur d'intégrité : " + str(e.orig))

    # Créer l'utilisateur lié
    hashed_password = hash_password(account_data.password)
    user = User(
        email=account_data.email,
        username=account_data.username,
        hashed_password=hashed_password,
        account_id=account.id  # lie user à l'account
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)  # 🟢 refresh pour obtenir l'ID
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erreur lors de la création de l'utilisateur : " + str(e.orig))

    db.refresh(account)  # 🟢 très important : met à jour la relation account.user
    return account
