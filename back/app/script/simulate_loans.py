import random
import uuid
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.book import Book
from app.models.loan import Loan
from app.models.role import Role

# =========================
# PARAMÈTRES
# =========================
START_YEAR = 2020
END_YEAR = 2026

NB_BORROWERS = 20
NB_STAFF = 5

MIN_LOANS_PER_USER = 5
MAX_LOANS_PER_USER = 40

# Taux de statuts
REQUESTED_RATE = 0.10
APPROVED_RATE  = 0.10
ONGOING_RATE   = 0.15
RETURNED_RATE  = 0.50
LATE_RATE      = 0.15

# =========================
# UTILS
# =========================
def random_date(year: int) -> date:
    return date(
        year,
        random.randint(1, 12),
        random.randint(1, 28)
    )

# =========================
# SCRIPT PRINCIPAL
# =========================
def main():
    db: Session = SessionLocal()

    try:
        print("Chargement des données...")

        borrowers = db.query(User).join(Role).filter(Role.name.in_(["Student", "Teacher"])).limit(NB_BORROWERS).all()
        staff_members = db.query(User).join(Role).filter(Role.name.in_(["Librarian", "Admin"])).limit(NB_STAFF).all()
        books = db.query(Book).all()

        if not borrowers or not staff_members or not books:
            raise RuntimeError("Alerte: Données insuffisantes pour la simulation")

        print(f"👤 Borrowers utilisés : {len(borrowers)}")
        print(f"🧑‍💼 Staff utilisés : {len(staff_members)}")
        print(f"📘 Livres disponibles : {len(books)}")

        total_loans = 0

        for borrower in borrowers:
            loan_count = random.randint(MIN_LOANS_PER_USER, MAX_LOANS_PER_USER)

            for _ in range(loan_count):
                book = random.choice(books)
                if book.quantity <= 0:
                    continue

                staff = random.choice(staff_members)
                year = random.randint(START_YEAR, END_YEAR)
                loan_request_date = random_date(year)
                due_date = loan_request_date + timedelta(days=random.randint(14, 30))

                # --- Statut ---
                r = random.random()
                status = None
                approved_by_id = None
                loan_date_val = loan_request_date  # Toujours défini
                return_date_val = None

                if r < REQUESTED_RATE:
                    status = "requested"
                    approved_by_id = None

                elif r < REQUESTED_RATE + APPROVED_RATE:
                    status = "approved"
                    approved_by_id = staff.id

                elif r < REQUESTED_RATE + APPROVED_RATE + ONGOING_RATE:
                    status = "ongoing"
                    approved_by_id = staff.id

                elif r < REQUESTED_RATE + APPROVED_RATE + ONGOING_RATE + RETURNED_RATE:
                    status = "returned"
                    approved_by_id = staff.id
                    return_date_val = due_date - timedelta(days=random.randint(0, 5))

                else:
                    status = "late"
                    approved_by_id = staff.id
                    return_date_val = due_date + timedelta(days=random.randint(1, 20))

                # Création du prêt
                loan = Loan(
                    user_id=borrower.id,
                    book_id=book.id,
                    approved_by_id=approved_by_id,
                    ticket=str(uuid.uuid4()),
                    loan_date=loan_date_val,
                    due_date=due_date,
                    return_date=return_date_val,
                    status=status
                )

                # Mise à jour du stock uniquement si le livre est retiré
                if status in ["ongoing", "returned", "late"]:
                    book.quantity -= 1

                db.add(loan)
                total_loans += 1

        db.commit()

        print("✅ Simulation terminée")
        print(f"Emprunts créés : {total_loans}")
        print(f"📅 Période : {START_YEAR} → {END_YEAR}")

    except Exception as e:
        db.rollback()
        print("❌ Erreur :", e)

    finally:
        db.close()

# =========================
# LANCEMENT
# =========================
if __name__ == "__main__":
    main()
