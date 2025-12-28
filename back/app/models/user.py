import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Permissions/roles
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    role = relationship("Role", back_populates="users")

    # Permissions directes
    permissions = relationship(
        "Permission",
        secondary="user_permissions",
        back_populates="users"
    )

    # Lien vers la personne
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True)
    account = relationship("Account", back_populates="user")

    # prêts en tant qu'emprunteur
    borrowed_loans = relationship(
        "Loan",
        foreign_keys="Loan.user_id",
        back_populates="borrower"
    )

    # prêts approuvés en tant que staff
    approved_loans = relationship(
        "Loan",
        foreign_keys="Loan.approved_by_id",
        back_populates="approved_by"
    )


    def has_permission(self, *permission_names: str) -> bool:
        if self.is_superuser:
            return True

        user_permissions = {p.name for p in self.permissions}

        if self.role:
            user_permissions |= {p.name for p in self.role.permissions}

        return any(name in user_permissions for name in permission_names)