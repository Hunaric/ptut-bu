from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.role import Role
from app.models.permission import Permission
from app.models.user import User

# Permissions de base
PERMISSIONS = [
    {"name": "loan:create", "description": "Créer un prêt"},
    {"name": "loan:approve", "description": "Approuver un prêt"},
    {"name": "loan:return", "description": "Enregistrer le retour d'un livre"},
    {"name": "loan:view_all", "description": "Voir tous les prêts"},
    {"name": "loan:manage", "description": "Gérer tous les prêts"},
    {"name": "loan:view_own", "description": "Voir ses propres emprunts"},
    {"name": "book:manage", "description": "Gérer les livres"},
]

# Rôles et leurs permissions par défaut
ROLES = {
    "Student": ["loan:create", "loan:view_own"],
    "Teacher": ["loan:create", "loan:approve"],
    "Librarian": ["loan:create", "loan:approve", "loan:return", "loan:view_all", "loan:manage", "book:manage"],
    "Admin": ["loan:create", "loan:approve", "loan:return", "loan:view_all", "loan:manage"],
}

def seed_roles_permissions():
    db: Session = SessionLocal()
    try:
        # Créer permissions si elles n'existent pas
        existing_permissions = {p.name: p for p in db.query(Permission).all()}
        for perm in PERMISSIONS:
            if perm["name"] not in existing_permissions:
                p = Permission(name=perm["name"], description=perm["description"])
                db.add(p)
                existing_permissions[perm["name"]] = p

        db.commit()

        # Créer les rôles si pas existants
        existing_roles = {r.name: r for r in db.query(Role).all()}
        for role_name, perm_names in ROLES.items():
            if role_name not in existing_roles:
                role = Role(name=role_name)
                # assigner les permissions
                role.permissions = [existing_permissions[p] for p in perm_names]
                db.add(role)

        db.commit()
        print("✅ Rôles et permissions créés avec succès")

    except Exception as e:
        db.rollback()
        print("❌ Erreur :", e)
    finally:
        db.close()


if __name__ == "__main__":
    seed_roles_permissions()
