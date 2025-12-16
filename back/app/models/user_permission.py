from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.database import Base

user_permissions = Table(
    "user_permissions",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True)
)
