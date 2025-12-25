# app/scripts/import_books_full.py

import random
import requests
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.book import Book
from app.models.category import Category
from app.models.tag import Tag

OPENLIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
OPENLIBRARY_WORK_URL = "https://openlibrary.org{work_key}.json"

BATCH_SIZE = 100
MIN_BOOKS_PER_CATEGORY = 50

# Liste de catégories avec requête associée
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


def get_cover_url(doc: dict) -> str | None:
    if doc.get("cover_i"):
        return f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-L.jpg"
    if doc.get("isbn"):
        return f"https://covers.openlibrary.org/b/isbn/{doc['isbn'][0]}-L.jpg"
    return None


def get_work_data(work_key: str) -> dict:
    """Récupère description et subjects depuis l'endpoint /works/OLXXXW.json"""
    try:
        r = requests.get(OPENLIBRARY_WORK_URL.format(work_key=work_key), timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}


def import_books():
    db: Session = SessionLocal()

    try:
        # Récupération des catégories et tags existants
        categories = {c.name.lower(): c for c in db.query(Category).all()}
        tags_cache = {t.name.lower(): t for t in db.query(Tag).all()}

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
                    OPENLIBRARY_SEARCH_URL,
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

                    # Récupérer description et subjects via /works/
                    work_key = doc.get("key")
                    work_data = get_work_data(work_key) if work_key else {}

                    description = None
                    if isinstance(work_data.get("description"), dict):
                        description = work_data["description"].get("value")
                    elif isinstance(work_data.get("description"), str):
                        description = work_data.get("description")

                    subjects = work_data.get("subjects", []) or doc.get("subject", [])

                    # Gestion tags
                    book_tags = []
                    for s in subjects[:5]:
                        tag_name = s[:100].lower()
                        tag = tags_cache.get(tag_name)
                        if not tag:
                            tag = Tag(name=s[:100])
                            db.add(tag)
                            db.flush()
                            tags_cache[tag_name] = tag
                        book_tags.append(tag)

                    # Création du livre
                    book = Book(
                        title=title,
                        author=doc.get("author_name", [None])[0],
                        description=description,
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
