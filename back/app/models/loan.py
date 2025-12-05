from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    # relations
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # dates
    loan_date = Column(Date, nullable=False)            # date du prêt
    due_date = Column(Date, nullable=False)             # date limite pour rendre
    return_date = Column(Date, nullable=True)           # date réelle de retour

    # statut
    status = Column(String(50), nullable=False, default="ongoing")  
    # exemples : "ongoing", "returned", "late"

    # relations ORM
    book = relationship("Book", back_populates="loans")
    user = relationship("User", back_populates="loans")
