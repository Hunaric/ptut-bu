# app/models/account.py

import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import Numeric


class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    
    sexe = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    etablissement = Column(String, nullable=False)

    # Adresse
    numero = Column(String, nullable=True)
    rue = Column(String, nullable=True)
    boite_postale = Column(String, nullable=True)
    code_postal = Column(String, nullable=True)
    ville = Column(String, nullable=True)
    codex_ville = Column(String, nullable=True)
    pays = Column(String, nullable=True)

    # Contact
    telephone = Column(String, nullable=True)

    # Relation avec l'utilisateur (optionnelle)
    user = relationship("User", back_populates="account", uselist=False)
