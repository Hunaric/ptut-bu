// loan.model.ts
export type LoanStatus =
  | 'requested'
  | 'approved'
  | 'ongoing'
  | 'returned'
  | 'late';

export interface Loan {
  id: number;
  book_id: number;
  user_id: string;        // UUID

  loan_date?: string;     // ISO date
  due_date?: string;
  return_date?: string;

  status: LoanStatus;
  ticket?: string;

  book_quantity?: number;
}

export interface LoanFilter {
  student_ids?: string[];
  status?: string;
  overdue?: boolean;
  start_date?: string;
  end_date?: string;
}
