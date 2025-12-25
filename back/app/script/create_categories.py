from app.core.database import SessionLocal
from app.models.category import Category

CATEGORIES = [
    "Science Fiction",
    "Fantasy",
    "Romance",
    "Thriller",
    "Mystery",
    "Crime",
    "Horror",
    "Adventure",
    "Historical",
    "Biography",
    "Autobiography",
    "Poetry",
    "Drama",
    "Comics",
    "Graphic Novel",
    "Children",
    "Young Adult",
    "Education",
    "Philosophy",
    "Religion",
    "Psychology",
    "Self Help",
    "Business",
    "Economics",
    "Politics",
    "Science",
    "Technology",
    "Computer Science",
    "Mathematics",
    "Medicine",
    "Art",
    "Music",
    "Photography",
    "Travel",
    "Cooking",
    "Sports",
    "True Crime",
    "Other"  # fallback obligatoire
]


def create_categories():
    db = SessionLocal()
    try:
        existing = {c.name.lower() for c in db.query(Category).all()}
        created = 0

        for name in CATEGORIES:
            if name.lower() not in existing:
                db.add(Category(name=name))
                existing.add(name.lower())
                created += 1

        db.commit()
        print(f"✅ {created} catégories créées")

    except Exception as e:
        db.rollback()
        print("❌ Erreur :", e)
    finally:
        db.close()


if __name__ == "__main__":
    create_categories()
