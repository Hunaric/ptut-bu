export interface DashboardStats {
  loans_by_month: number[];
  on_time_return_rate: number;
  metrics: {
    total_books: number;
    total_loans: number;
    active_loans: number;
    late_loans: number;
  on_time_return_rate: number;
  };
}
