import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { Loan } from '../../interfaces/loan';
import { LoanService } from '../../services/loan.service';
import { Book, BorrowedBook } from '../../interfaces/book';
import { PageBreadcrumbComponent } from '../../components/common/page-breadcrumb/page-breadcrumb.component';

@Component({
  selector: 'app-my-loans',
  standalone: true,
  imports: [CommonModule, DatePipe, PageBreadcrumbComponent],
  templateUrl: './my-loans.component.html',
  styleUrls: ['./my-loans.component.css']
})
export class MyLoansComponent implements OnInit {

  loans: BorrowedBook[] = [];
  loading = true;
  error: string | null = null;

  constructor(private loanService: LoanService) {}

  ngOnInit(): void {
    this.fetchLoans();
  }

  async fetchLoans() {
    this.loading = true;
    this.error = null;

    try {
      this.loans = await this.loanService.getMyLoans();
      // Tri du plus récent au plus ancien
    } catch (err) {
      console.error(err);
      this.error = "Impossible de récupérer vos emprunts.";
    } finally {
      this.loading = false;
    }
  }


  getStatusLabel(status: string): string {
    switch (status) {
      case 'approved': return 'Approuvé';
      case 'ongoing': return 'En cours';
      case 'requested': return 'Demandé';
      case 'late': return 'En retard';
      default: return status;
    }
  }

  getStatusColor(status: string): string {
    switch (status) {
      case 'approved': return 'bg-green-100 text-green-800';
      case 'ongoing': return 'bg-blue-100 text-blue-800';
      case 'requested': return 'bg-yellow-100 text-yellow-800';
      case 'late': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }

}
