from uuid import UUID
from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    # relations
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # dates
    loan_date = Column(Date, nullable=False)            # date du prêt
    due_date = Column(Date, nullable=False)             # date limite pour rendre
    return_date = Column(Date, nullable=True)           # date réelle de retour

    # statut
    status = Column(String(50), nullable=False, default="requested")  
    # "requested", "approved", "ongoing", "returned", "late"


    # Ticket pour récupérer le livre
    ticket = Column(String(36), nullable=True, unique=True)

    # relations ORM
    book = relationship("Book", back_populates="loans")
    user = relationship("User", back_populates="loans")


