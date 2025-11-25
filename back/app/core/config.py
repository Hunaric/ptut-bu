import os

POSTGRES_USER = os.getenv("POSTGRES_USER", "ptut_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "ptut_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ptut_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
