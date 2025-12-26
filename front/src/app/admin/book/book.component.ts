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
  console.log('Appel à loadBooks(), page actuelle :', this.page);
  this.loading = true;
  try {
    const res: PaginatedResponse<Book> = await this.bookService.getBooksAdvanced(this.page, this.size);
    this.books = res.items;
    this.totalPages = Math.ceil(res.total / res.size);
    this.page = res.page;
    console.log("Lui");
    
  } catch (err) {
    console.error('Erreur lors du chargement des livres', err);
  } finally {
    console.log("MOi");
    
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

trackById(index: number, book: Book) {
  return book.id;
}


}

