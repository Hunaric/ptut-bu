import { Component, Input } from '@angular/core';
import { Category } from '../../interfaces/category';
import { Tag } from '../../interfaces/tag';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { BookService } from '../../services/book.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-crud-book',
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './crud-book.component.html',
  styleUrl: './crud-book.component.css',
})
export class CrudBookComponent {
  
  bookId?: number;
  categories: Category[] = [];
  tags: Tag[] = [];

  bookForm = new FormGroup({
    title: new FormControl('', [Validators.required]),
    author: new FormControl(''),
    description: new FormControl(''),
    isbn: new FormControl(''),
    published_year: new FormControl(''),
    category_id: new FormControl<number | null>(null),
    quantity: new FormControl(1, [Validators.min(1)]),
    tags: new FormControl<number[]>([])
  });


  constructor(private bookService: BookService, private router: Router, private route: ActivatedRoute) {}


  ngOnInit(): void {
    this.loadCategories();
    this.loadTags();
    // console.log(this.loadTags);
    

    // Récupération de l'ID depuis l'URL
    this.route.paramMap.subscribe(params => {
        const id = params.get('id');
        if (id) {
            this.bookId = +id;
            this.loadBook(); // charger les données pour édition
        }
    });
  }

  async loadCategories() {
    try {
      this.categories = await this.bookService.getCategories();
    } catch (err) {
      console.error('Erreur chargement catégories', err);
    }
  }

  async loadTags() {
    try {
      this.tags = await this.bookService.getTags();
    } catch (err) {
      console.error('Erreur chargement tags', err);
    }
  }

  async loadBook() {
    if (!this.bookId) return;
    try {
      const book = await this.bookService.getBookById(this.bookId);
      this.bookForm.patchValue({
        title: book.title,
        author: book.author,
        description: book.description,
        isbn: book.isbn,
        published_year: book.published_year,
        category_id: book.category?.id,
        quantity: book.quantity,
        tags: book.tag?.map(t => t.id) || []
      });
    } catch (err) {
      console.error('Erreur chargement livre', err);
    }
  }


onTagChange(event: Event) {
  const input = event.target as HTMLInputElement;
  let selectedTags: number[] = this.bookForm.value.tags || [];
  const value = Number(input.value);
  if (input.checked) {
    selectedTags.push(value);
  } else {
    selectedTags = selectedTags.filter(id => id !== value);
  }
  this.bookForm.patchValue({ tags: selectedTags });
}

  async submitForm() {
    const payload = {
  ...this.bookForm.value,
  category_id: this.bookForm.value.category_id ?? undefined,
  title: this.bookForm.value.title ?? undefined,
  author: this.bookForm.value.author ?? undefined,
  description: this.bookForm.value.description ?? undefined,
  isbn: this.bookForm.value.isbn ?? undefined,
  published_year: this.bookForm.value.published_year ?? undefined,
  quantity: this.bookForm.value.quantity ?? undefined,
  tags: this.bookForm.value.tags 
};

    if (!this.bookForm.valid) return;

    try {
      if (this.bookId) {
  await this.bookService.updateBook(this.bookId, payload);
} else {
  await this.bookService.createBook(payload);
}

      this.router.navigate(['/books']);
    } catch (err) {
      console.error('Erreur sauvegarde livre', err);
    }
  }
}
