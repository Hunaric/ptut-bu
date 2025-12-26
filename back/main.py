from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, book, user, category, role, permission, loan, calendar
from app.core.database import Base, engine
from app.models.user import User
from app.models.role import Role
from app.models.account import Account
from app.models.permission import Permission 
from app.models.user_permission import user_permissions   
from app.models.category import Category
from app.models.book import Book
from app.models.tag import Tag
from app.models.book_tag import book_tag
from app.models.loan import Loan
from app.models.calendar_event import CalendarEvent
# from app.models.role_permission import RolePermission


# Crée les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bibliotheque Universitaire")

origins = [
    "http://localhost:4300",  # Angular dev server
    "http://localhost:4200",  # si utilisé
    "http://127.0.0.1:4300",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ou ["*"] pour autoriser toutes les origines (pas recommandé en prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(book.router)
app.include_router(user.router) 
app.include_router(auth.router) 
app.include_router(category.router)
app.include_router(role.router)
app.include_router(permission.router)
app.include_router(loan.router)
app.include_router(calendar.router)

@app.get("/books")
async def get_books():
    return [{"id": 1, "title": "Book 1"}, {"id": 2, "title": "Book 2"}]