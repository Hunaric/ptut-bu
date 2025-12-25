from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.book import Book

def clear_books():
    db: Session = SessionLocal()
    try:
        deleted = db.query(Book).delete()
        db.commit()
        print(f"✅ {deleted} livres supprimés")
    except Exception as e:
        db.rollback()
        print("❌ Erreur :", e)
    finally:
        db.close()

if __name__ == "__main__":
    clear_books()
