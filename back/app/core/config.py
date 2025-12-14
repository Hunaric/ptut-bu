import os

POSTGRES_USER = os.getenv("POSTGRES_USER", "ptut_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "ptut_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ptut_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

# app/core/config.py

from dotenv import load_dotenv
import os

load_dotenv()  # Charge les variables d'environnement depuis le fichier .env

class Settings:
    PROJECT_NAME: str = "Banking API"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()
