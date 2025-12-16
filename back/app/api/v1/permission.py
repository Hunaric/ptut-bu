from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.permission import create_permission, get_permissions
from app.schemas.permission import PermissionCreate, PermissionResponse

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.post("/", response_model=PermissionResponse)
def add_permission(perm: PermissionCreate, db: Session = Depends(get_db)):
    return create_permission(db, perm)

@router.get("/", response_model=list[PermissionResponse])
def list_permissions(db: Session = Depends(get_db)):
    return get_permissions(db)
    