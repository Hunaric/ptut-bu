from sqlalchemy.orm import Session
from app.models import user, person
from app.schemas import user as user_schema
from app.core.security import hash_password

def create_user(db: Session, user_in: user_schema.UserCreate):
    hashed_password = hash_password(user_in.password)
    db_user = user.User(
        email_etablissement=user_in.email_etablissement,
        username=user_in.username,
        hashed_password=hashed_password,
        person_id=user_in.person_id,
        role_id=user_in.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(user.User).filter(user.User.id == user_id).first()
