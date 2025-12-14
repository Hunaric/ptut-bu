from app.api.v1 import auth
from fastapi import FastAPI
from app.api.v1 import book, user
from app.core.database import Base, engine
from app.models.user import User
from app.models.role import Role
from app.models.account import Account

# Crée les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bibliotheque Universitaire")

# Routes
app.include_router(book.router, prefix="/books", tags=["Books"])
app.include_router(user.router) 
app.include_router(auth.router) 

@app.get("/books")
async def get_books():
    return [{"id": 1, "title": "Book 1"}, {"id": 2, "title": "Book 2"}]