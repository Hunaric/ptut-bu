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
    const res: PaginatedResponse<Book> = await this.bookService.getBooksAdvanced(this.page, this.size);
    this.books = res.items;
    this.totalPages = Math.ceil(res.total / res.size);
    this.page = res.page;
    
  } catch (err) {
    console.error('Erreur lors du chargement des livres', err);
  } finally {
    
    this.loading = false;
  }
}
goToPage(value: string | number) {
  let pageNumber = Number(value);

  // Valider la valeur
  if (isNaN(pageNumber) || pageNumber < 1) {
    pageNumber = 1;
  } else if (pageNumber > this.totalPages) {
    pageNumber = this.totalPages;
  }

  this.page = pageNumber;
  this.loadBooks();
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

trackById(index: number, book: Book) {
  return book.id;
}


}

