# app/models/book_tag.py

from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.database import Base

book_tag = Table(
    "book_tag",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
