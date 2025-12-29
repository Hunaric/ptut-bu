import { Component, OnInit } from '@angular/core';
import { LoanService } from '../../services/loan.service';
import { Loan, LoanList } from '../../interfaces/loan'; // <-- utilise Loan, pas LoanCalendar
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-loan-list',
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './loan-list.component.html',
  styleUrls: ['./loan-list.component.css']
})
export class LoanListComponent implements OnInit {

  loans: LoanList[] = [];
  loading = false;
  error: string | null = null;


page = 1;
pageInput = 1; // input lié au formulaire
pageSize = 20;
total = 0;

  constructor(private loanService: LoanService) {}

  
  async ngOnInit() {
    await this.loadLoans();
  }

async loadLoans() {
  this.loading = true;
  try {
    const response = await this.loanService.getAllLoans(this.page, this.pageSize);
    this.loans = response.data;
    this.total = response.total;
    this.pageInput = this.page; // synchroniser input avec page actuelle
  } catch (err) {
    this.error = 'Erreur lors du chargement des prêts';
    console.error(err);
  } finally {
    this.loading = false;
  }
}

async changePage(newPage: number) {
  if (newPage < 1) newPage = 1;
  if (newPage > this.totalPages) newPage = this.totalPages;
  this.page = newPage;
  await this.loadLoans();
}

async goToPage() {
  let newPage = Math.floor(this.pageInput);
  if (newPage < 1) newPage = 1;
  if (newPage > this.totalPages) newPage = this.totalPages;
  this.page = newPage;
  await this.loadLoans();
}

get totalPages(): number {
  return Math.ceil(this.total / this.pageSize) || 1;
}


  async markAsReturned(loan: LoanList) {
    try {
      await this.loanService.updateLoanStatus(loan.id, 'returned'); // conforme à la signature du service
      loan.status = 'returned';
    } catch (err) {
      console.error('Impossible de mettre à jour le statut', err);
    }
  }

  async approveLoan(loan: LoanList) {
    try {
      await this.loanService.updateLoanStatus(loan.id, 'approved');
      loan.status = 'approved';
    } catch (err) {
      console.error('Impossible de valider le prêt', err);
    }
  }

statusLabels: Record<string, string> = {
  requested: 'Demandé',
  approved: 'Approuvé',
  ongoing: 'En cours',
  returned: 'Rendu',
  late: 'En retard'
};

statusColors: Record<string, string> = {
  requested: 'text-blue-600',
  approved: 'text-green-600',
  ongoing: 'text-yellow-600',
  returned: 'text-gray-600',
  late: 'text-red-600'
};


  // async rejectLoan(loan: Loan) {
  //   try {
  //     await this.loanService.updateLoanStatus(loan.id, 'rejected');
  //     loan.status = 'rejected';
  //   } catch (err) {
  //     console.error('Impossible de rejeter le prêt', err);
  //   }
  // }

  // async extendLoan(loan: Loan) {
  //   try {
  //     await this.loanService.updateLoanStatus(loan.id, 'extended');
  //     loan.status = 'extended';
  //   } catch (err) {
  //     console.error('Impossible de prolonger le prêt', err);
  //   }
  // }
}
