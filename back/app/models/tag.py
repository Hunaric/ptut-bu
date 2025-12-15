# app/models/tag.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.book_tag import book_tag

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True, nullable=False)

    books = relationship(
        "Book",
        secondary=book_tag,
        back_populates="tags"
    )
