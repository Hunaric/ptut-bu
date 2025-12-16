from sqlalchemy.orm import Session
from app.models.loan import Loan
from app.schemas.loan import LoanFilter 

def query_loans(db: Session, filters: LoanFilter):
    query = db.query(Loan)

    if filters.student_ids:
        query = query.filter(Loan.user_id.in_(filters.student_ids))
    if filters.returned is not None:
        query = query.filter(Loan.returned == filters.returned)
    if filters.overdue:
        from datetime import datetime
        query = query.filter(Loan.due_date < datetime.now(), Loan.returned == False)

    return query.all()
