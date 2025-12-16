from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.permission import Permission
from app.schemas.role import RoleCreate

def create_role(db: Session, role_data: RoleCreate):
    role = Role(name=role_data.name, description=role_data.description)
    if role_data.permission_ids:
        perms = db.query(Permission).filter(Permission.id.in_(role_data.permission_ids)).all()
        role.permissions = perms
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def get_roles(db: Session):
    return db.query(Role).all()

def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()
