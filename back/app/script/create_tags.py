from app.core.database import SessionLocal
from app.models.tag import Tag

TAGS = [
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
    "Artificial Intelligence",
    "Computer Science",
    "Programming",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Medicine",
    "Art",
    "Music",
    "Photography",
    "Travel",
    "Cooking",
    "Sports",
    "True Crime",
    "Classic",
    "Dystopia",
    "Post Apocalyptic",
    "Space",
    "Robots",
    "Time Travel"
]


def create_tags():
    db = SessionLocal()
    try:
        existing = {t.name.lower() for t in db.query(Tag).all()}
        created = 0

        for name in TAGS:
            if name.lower() not in existing:
                db.add(Tag(name=name))
                existing.add(name.lower())
                created += 1

        db.commit()
        print(f"🏷️ {created} tags créés")

    except Exception as e:
        db.rollback()
        print("❌ Erreur :", e)
    finally:
        db.close()


if __name__ == "__main__":
    create_tags()
