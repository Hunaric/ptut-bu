// loan.model.ts
export type LoanStatus =
  | 'requested'
  | 'approved'
  | 'ongoing'
  | 'returned'
  | 'late';

export interface Loan {
book_title: any;
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

export interface LoanList {
  id: number;
  book_id: number;
  user_id: string;
  book_title?: string;
  borrower_name?: string;
  loan_date?: string;
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

export interface LoanCalendar {
  id: number;
  book_title: string;
  due_date: string;
  borrower_name?: string;
  status: LoanStatus;
}