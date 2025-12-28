from app.models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import tag as crud
from app.schemas.tag import TagSimple
from app.core.dependencies import require_admin, require_superuser
from app.core.database import get_db

router = APIRouter()

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("/", response_model=list[TagSimple])
def list_tag(db: Session = Depends(get_db)):
    return crud.get_tags(db)
