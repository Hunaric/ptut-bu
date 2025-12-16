from sqlalchemy.orm import Session
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate

def create_permission(db: Session, perm: PermissionCreate):
    p = Permission(name=perm.name, description=perm.description)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def get_permissions(db: Session):
    return db.query(Permission).all()
