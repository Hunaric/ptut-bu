from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str | None = None

class BookCreate(BookBase):
    pass
class Book(BaseModel):
    id: int
    title: str

    model_config = {
        "from_attributes": True
    }
