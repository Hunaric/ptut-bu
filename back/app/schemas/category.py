from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str

class Category(CategoryBase):
    id: int

    model_config = {
        "from_attributes": True
    }
