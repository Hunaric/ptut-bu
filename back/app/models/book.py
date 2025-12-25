from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.book_tag import book_tag

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    isbn = Column(String(20), unique=True, nullable=True)
    published_year = Column(Integer, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    quantity = Column(Integer, nullable=False, default=1)

    cover_url = Column(String(500), nullable=True)

    # Relation vers Category
    category = relationship("Category", back_populates="books")
    # Relation vers BorrowRecord        
    # borrow_records = relationship("BorrowRecord", back_populates="book")    
    loans = relationship("Loan", back_populates="book")

    tags = relationship(
        "Tag",
        secondary=book_tag,
        back_populates="books"
    )
    