import random
import requests
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.book import Book
from app.models.category import Category
from app.models.tag import Tag

OPENLIBRARY_URL = "https://openlibrary.org/search.json"
BATCH_SIZE = 100
MIN_BOOKS_PER_CATEGORY = 50

# Catégories et requêtes OpenLibrary
QUERIES = {
    "Science Fiction": "science fiction",
    "Fantasy": "fantasy",
    "Romance": "romance",
    "Thriller": "thriller",
    "Mystery": "mystery",
    "History": "history",
    "Biography": "biography",
    "Horror": "horror",
    "Children": "children",
    "Young Adult": "young adult",
}


def get_subjects(doc: dict) -> list[str]:
    """Récupère la liste de sujets d’un document OpenLibrary."""
    return doc.get("subject") or doc.get("subject_facet") or []


def get_cover_url(doc: dict) -> str | None:
    """Récupère l'URL de couverture d’un document."""
    if doc.get("cover_i"):
        return f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-L.jpg"
    if doc.get("isbn"):
        return f"https://covers.openlibrary.org/b/isbn/{doc['isbn'][0]}-L.jpg"
    return None


def import_books():
    db: Session = SessionLocal()
    try:
        # Récupérer toutes les catégories et tags existants
        categories = {c.name.lower(): c for c in db.query(Category).all()}
        tags = {t.name.lower(): t for t in db.query(Tag).all()}

        other_category = categories.get("other")
        if not other_category:
            raise Exception("❌ La catégorie 'Other' doit exister")

        total_imported = 0

        for category_name, query in QUERIES.items():
            print(f"\n📚 Import catégorie : {category_name}")
            category = categories.get(category_name.lower(), other_category)
            imported_for_category = 0
            page = 1

            while imported_for_category < MIN_BOOKS_PER_CATEGORY:
                r = requests.get(
                    OPENLIBRARY_URL,
                    params={"q": query, "page": page, "limit": BATCH_SIZE},
                    timeout=15
                )
                r.raise_for_status()

                docs = r.json().get("docs", [])
                if not docs:
                    break

                for doc in docs:
                    if imported_for_category >= MIN_BOOKS_PER_CATEGORY:
                        break

                    isbn = doc.get("isbn", [None])[0]
                    if isbn and db.query(Book).filter(Book.isbn == isbn).first():
                        continue

                    title = doc.get("title")
                    if not title:
                        continue

                    # Récupérer les tags existants correspondants
                    subjects = get_subjects(doc)
                    book_tags = [tags[s[:100].lower()] for s in subjects[:5] if s[:100].lower() in tags]

                    book = Book(
                        title=title,
                        author=doc.get("author_name", [None])[0],
                        description=None,
                        isbn=isbn,
                        published_year=doc.get("first_publish_year"),
                        cover_url=get_cover_url(doc),
                        quantity=random.randint(0, 15),
                        category=category,
                        tags=book_tags
                    )

                    db.add(book)
                    imported_for_category += 1
                    total_imported += 1

                page += 1

            print(f"✅ {imported_for_category} livres importés pour {category_name}")

        db.commit()
        print(f"\n🎉 Import terminé : {total_imported} livres au total")

    except Exception as e:
        db.rollback()
        print("❌ Erreur :", e)
    finally:
        db.close()


if __name__ == "__main__":
    import_books()
