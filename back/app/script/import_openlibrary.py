import requests
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.book import Book
from app.models.tag import Tag
from app.models.category import Category

OPENLIBRARY_URL = "https://openlibrary.org/search.json"
BATCH_SIZE = 100


def get_subjects(doc) -> list[str]:
    """
    OpenLibrary fiable :
    subject_facet > subject > []
    """
    return (
        doc.get("subject_facet")
        or doc.get("subject")
        or []
    )


def get_cover_url(doc):
    if doc.get("cover_i"):
        return f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-L.jpg"
    if doc.get("isbn"):
        return f"https://covers.openlibrary.org/b/isbn/{doc['isbn'][0]}-L.jpg"
    return None


def ensure_entities(db: Session, model, names: set[str]) -> dict[str, int]:
    existing = db.query(model).all()
    mapping = {e.name: e.id for e in existing}

    for name in names:
        if name not in mapping:
            obj = model(name=name)
            db.add(obj)
            db.flush()          # IMPORTANT
            mapping[name] = obj.id

    db.commit()
    return mapping


def import_books(query: str, pages: int = 5):
    db = SessionLocal()

    try:
        all_docs = []

        # 1️⃣ Télécharger les données
        for page in range(1, pages + 1):
            print(f"📦 Page {page}")
            r = requests.get(
                OPENLIBRARY_URL,
                params={"q": query, "page": page, "limit": BATCH_SIZE},
                timeout=15
            )
            r.raise_for_status()
            all_docs.extend(r.json().get("docs", []))

        # 2️⃣ Collecter catégories & tags
        category_names = set()
        tag_names = set()

        for doc in all_docs:
            subjects = get_subjects(doc)
            if subjects:
                category_names.add(subjects[0][:100])
                for s in subjects[:5]:
                    tag_names.add(s[:100])

        print(f"📚 Catégories détectées : {len(category_names)}")
        print(f"🏷️ Tags détectés : {len(tag_names)}")

        # 3️⃣ Créer catégories & tags
        category_ids = ensure_entities(db, Category, category_names)
        tag_ids = ensure_entities(db, Tag, tag_names)

        # 4️⃣ Créer les livres
        imported = 0

        for doc in all_docs:
            isbn = doc.get("isbn", [None])[0]
            if isbn and db.query(Book).filter(Book.isbn == isbn).first():
                continue

            title = doc.get("title")
            if not title:
                continue

            subjects = get_subjects(doc)

            book = Book(
                title=title,
                author=doc.get("author_name", [None])[0],
                description=None,
                isbn=isbn,
                published_year=doc.get("first_publish_year"),
                cover_url=get_cover_url(doc)
            )

            # catégorie
            if subjects:
                book.category_id = category_ids.get(subjects[0][:100])

            # tags
            if subjects:
                book.tags = (
                    db.query(Tag)
                    .filter(Tag.id.in_([
                        tag_ids[s[:100]] for s in subjects[:5] if s[:100] in tag_ids
                    ]))
                    .all()
                )

            db.add(book)
            imported += 1

        db.commit()
        print(f"🎉 Import terminé : {imported} livres")

    except Exception as e:
        db.rollback()
        print("❌ Erreur :", e)

    finally:
        db.close()


if __name__ == "__main__":
    import_books("science fiction", pages=5)
