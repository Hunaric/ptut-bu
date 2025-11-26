from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
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
    email = Column(String, unique=True, index=True, nullable=False)
    telephone = Column(String, nullable=True)

    # Relation avec l'utilisateur (optionnelle)
    user = relationship("User", back_populates="person", uselist=False)
