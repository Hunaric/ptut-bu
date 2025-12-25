# app/schemas/book.py
from typing import Optional, List
from pydantic import BaseModel

class TagSimple(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }
