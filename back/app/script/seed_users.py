import random
from faker import Faker
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.account import AccountCreate
from app.crud.account import create_account
from app.models.role import Role
from fastapi import HTTPException

fake = Faker()

N_USERS = 20  # nombre d'utilisateurs à générer

SEXE_OPTIONS = ["M", "F"]
ROLES = ["Student", "Teacher", "Librarian", "Admin"]  # rôles possibles
ETABLISSEMENTS = [
    "Université de Paris",
    "Université de Lyon",
    "Université de Marseille",
    "Université de Toulouse",
    "Université de Bordeaux",
]

def seed_users_with_roles():
    db: Session = SessionLocal()
    created = 0

    try:
        # récupérer les rôles existants
        roles = {r.name: r for r in db.query(Role).all()}

        for _ in range(N_USERS):
            sexe = random.choice(SEXE_OPTIONS)
            prenom = fake.first_name_male() if sexe == "M" else fake.first_name_female()
            nom = fake.last_name()
            email = fake.unique.email()
            username = fake.unique.user_name()
            password = "Password123!"
            etablissement = random.choice(ETABLISSEMENTS)
            role_name = random.choice(ROLES)
            role = roles.get(role_name)

            account_data = AccountCreate(
                sexe=sexe,
                prenom=prenom,
                nom=nom,
                email=email,
                username=username,
                password=password,
                etablissement=etablissement,
                numero=str(fake.building_number()),
                rue=fake.street_name(),
                boite_postale=fake.postcode(),
                code_postal=fake.postcode(),
                ville=fake.city(),
                codex_ville=fake.postcode(),
                pays=fake.country(),
                telephone=fake.phone_number(),
            )

            try:
                account = create_account(db, account_data)
                # assigner le rôle
                if role:
                    account.user.role = role
                created += 1
            except HTTPException as e:
                print(f"⚠️ Utilisateur {email} non créé: {e.detail}")

        db.commit()
        print(f"\n✅ {created} utilisateurs créés avec des rôles variés")

    finally:
        db.close()


if __name__ == "__main__":
    seed_users_with_roles()
