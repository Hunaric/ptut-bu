from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    # emprunteur
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # staff qui approuve
    approved_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    loan_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    status = Column(String(50), nullable=False, default="requested")
    ticket = Column(String(36), nullable=True, unique=True)

    # relations
    book = relationship("Book", back_populates="loans")

    borrower = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="borrowed_loans"
    )

    approved_by = relationship(
        "User",
        foreign_keys=[approved_by_id],
        back_populates="approved_loans"
    )
