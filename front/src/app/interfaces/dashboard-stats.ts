export interface DashboardStats {
  scope: 'global' | 'user';
  loans_by_month: number[];
  late_by_month: number[];
  on_time_return_rate: number;
  metrics: {
    total_books: number;
    total_loans: number;
    active_loans: number;
    late_loans: number;
    return_rate: number;
  };
}
