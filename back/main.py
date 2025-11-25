from fastapi import FastAPI
from app.api.v1 import book
from app.core.database import Base, engine

# Crée les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bibliotheque Universitaire")

# Routes
app.include_router(book.router, prefix="/books", tags=["Books"])

@app.get("/books")
async def get_books():
    return [{"id": 1, "title": "Book 1"}, {"id": 2, "title": "Book 2"}]