import { Component, OnInit } from '@angular/core';
import { BookItemComponent } from './book-item/book-item.component';
import { PageBreadcrumbComponent } from '../../components/common/page-breadcrumb/page-breadcrumb.component';
import { CardComponent } from '../../shared/components/ui/card/card.component';
import { BookService } from '../../services/book.service';
import { Book } from '../../interfaces/book';
import { CommonModule } from '@angular/common';
import { PaginatedResponse } from '../../interfaces/paginated-response';

@Component({
  selector: 'app-book',
  standalone: true,
  imports: [
    PageBreadcrumbComponent,
    CardComponent,
    BookItemComponent, 
    CommonModule
  ],
  templateUrl: './book.component.html',
  styleUrl: './book.component.css',
})
export class BookComponent implements OnInit {

  books: Book[] = [];

  // pagination
  page = 1;
  size = 8;
  totalPages = 0;
  loading = false;

  constructor(private bookService: BookService) {}

  ngOnInit(): void {
    this.loadBooks();
  }

  async loadBooks(): Promise<void> {
  this.loading = true;

  try {
    // Appel au service pour récupérer les livres avec pagination
    const res: PaginatedResponse<Book> = await this.bookService.getBooksAdvanced(this.page, this.size);

    // On met à jour les données
    this.books = res.items;
    this.totalPages = res.pages;
  } catch (error) {
    if (error instanceof Error) {
      alert('Erreur lors du chargement des livres : ' + error.message);
    } else {
      alert('Erreur lors du chargement des livres');
    }
  } finally {
    this.loading = false;
  }
}

  nextPage() {
    if (this.page < this.totalPages) {
      this.page++;
      this.loadBooks();
    }
  }

  prevPage() {
    if (this.page > 1) {
      this.page--;
      this.loadBooks();
    }
  }

}
