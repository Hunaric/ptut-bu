import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BookService } from '../../services/book.service';
import { Book } from '../../interfaces/book';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import { PageBreadcrumbComponent } from '../../components/common/page-breadcrumb/page-breadcrumb.component';
import { LoanService } from '../../services/loan.service';
import { Loan } from '../../interfaces/loan';
import { ModalComponent } from '../../shared/components/ui/modal/modal.component';

@Component({
  selector: 'app-detail-book',
  imports: [CommonModule, PageBreadcrumbComponent, ModalComponent],
  templateUrl: './detail-book.component.html',
  styleUrl: './detail-book.component.css',
})
export class DetailBookComponent implements OnInit{

  fallbackUrl = '/images/grid-image/image-03.png';
  permissions: string[] = [];
  
  book?: Book;
  loading = true;
  error = '';

  // Modal
  isModalOpen = false;
  modalMessage = '';

  constructor(
    private route: ActivatedRoute,
    private bookService: BookService,
    private router: Router,
    private loanService: LoanService,
    public authService: AuthService
  ) {
   this.permissions = this.authService.getPermissions() || [];
  }

  async ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));

    if (!id) {
      this.error = 'ID invalide';
      this.loading = false;
      return;
    }

    try {
      this.book = await this.bookService.getBookById(id);
    } catch {
      this.error = 'Livre introuvable';
    } finally {
      this.loading = false;
    }
  }

  editBook() {
    if (this.book) {
      this.router.navigate(['/crud-books', this.book.id]);
    }
  }

  goBack() {
    this.router.navigate(['/books']);
  }
async createLoan() {
  if (!this.book) return;

  try {
    const loan: Loan = await this.loanService.createLoan(this.book.id);

    // Recharger le livre depuis l'API
    this.book = await this.bookService.getBookById(this.book.id);

    this.modalMessage = `Livre emprunté avec succès ! Date de retour : ${loan.due_date}`;
  } catch (error: any) {
    this.modalMessage = error.error?.detail || 'Impossible de créer l’emprunt';
  } finally {
    this.isModalOpen = true;
  }
}

  closeModal() {
    this.isModalOpen = false;
  }
}
