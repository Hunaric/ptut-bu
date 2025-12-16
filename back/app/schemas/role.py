from typing import List
from pydantic import BaseModel
from app.schemas.permission import PermissionResponse

class RoleBase(BaseModel):
    name: str
    description: str | None = None

class RoleCreate(RoleBase):
    permission_ids: list[int] = []

class RoleResponse(RoleBase):
    id: int
    permissions: list[PermissionResponse] = []
    class Config:
        from_attributes = True
