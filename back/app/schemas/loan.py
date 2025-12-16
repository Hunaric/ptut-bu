from typing import Optional, List
from pydantic import BaseModel


class LoanFilter(BaseModel):
    student_ids: Optional[List[str]] = None
    returned: Optional[bool] = None
    overdue: Optional[bool] = None
