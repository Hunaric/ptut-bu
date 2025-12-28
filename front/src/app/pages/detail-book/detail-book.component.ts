import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BookService } from '../../services/book.service';
import { Book } from '../../interfaces/book';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-detail-book',
  imports: [CommonModule],
  templateUrl: './detail-book.component.html',
  styleUrl: './detail-book.component.css',
})
export class DetailBookComponent implements OnInit{

  fallbackUrl = '/images/grid-image/image-03.png';
  
  book?: Book;
  loading = true;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private bookService: BookService,
    private router: Router
  ) {}

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
}
