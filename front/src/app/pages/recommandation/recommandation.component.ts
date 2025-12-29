import { Component, OnInit } from '@angular/core';
import { PageBreadcrumbComponent } from '../../components/common/page-breadcrumb/page-breadcrumb.component';
import { CardComponent } from '../../shared/components/ui/card/card.component';
import { BookItemComponent } from '../../admin/book/book-item/book-item.component';
import { CommonModule } from '@angular/common';
import { Book } from '../../interfaces/book';
import { BookService } from '../../services/book.service';

@Component({
  selector: 'app-recommandation',
  imports: [
    PageBreadcrumbComponent,
    CardComponent,
    BookItemComponent, 
    CommonModule
  ],
  templateUrl: './recommandation.component.html',
  styleUrl: './recommandation.component.css',
})
export class RecommandationComponent implements  OnInit{
    books: Book[] = [];
  loading = false;
  
    constructor(private bookService: BookService) {}

  ngOnInit(): void {    
    this.loadRecommandedBooks();
  }
  
  async loadRecommandedBooks(): Promise<void> {
  this.loading = true;
  try {
    const books = await this.bookService.getUserRecommendations();
    this.books = books;
  } catch (err) {
    console.error('Erreur lors du chargement des recommandations', err);
  } finally {
    this.loading = false;
  }
}


}
