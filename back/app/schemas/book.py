from typing import Optional, List
from pydantic import BaseModel
from .category import Category
# =========================
# Base
# =========================

class BookBase(BaseModel):
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    category_id: Optional[int] = None
    quantity: Optional[int] = 1
    cover_url: Optional[str] = None

class RecommendedBook(BaseModel):
    id: int
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    category_id: Optional[int] = None
    quantity: Optional[int] = 1
    cover_url: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

# =========================
# Création
# =========================
class BookCreate(BookBase):
    tags: Optional[List[int]] = []   # IDs des tags


# =========================
# Mise à jour
# =========================
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    category_id: Optional[int] = None
    quantity: Optional[int] = None
    cover_url: Optional[str] = None
    tags: Optional[List[int]] = None

# =========================
# Réponse (lecture)
# =========================
class BookResponse(BookBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }

class TagSimple(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class BookResponseWithRelations(BookResponse):
    category: Optional[Category]
    tags: List[TagSimple] = []
    # loans: List[LoanResponse] = []


class BookFilter(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    published_after: Optional[int] = None
    published_before: Optional[int] = None
    category_ids: Optional[List[int]] = None
    tag_ids: Optional[List[int]] = None