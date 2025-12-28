from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.schemas.tag import TagSimple

def get_tags(db: Session):
    return db.query(Tag).all()
