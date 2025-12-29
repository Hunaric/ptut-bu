import { CommonModule } from '@angular/common';
import { Component, ElementRef, ViewChild } from '@angular/core';
import { SidebarService } from '../../services/sidebar.service';
import { ThemeToggleButtonComponent } from '../../components/common/theme-toggle-button/theme-toggle-button.component';
import { NotificationDropdownComponent } from '../../components/header/notification-dropdown/notification-dropdown.component';
import { UserDropdownComponent } from '../../components/header/user-dropdown/user-dropdown.component';
import { Book } from '../../../interfaces/book';
import { BookService } from '../../../services/book.service';
import { debounceTime, Subject } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { RouterLink } from "@angular/router";

@Component({
  selector: 'app-app-header',
  standalone: true,
  imports: [
    CommonModule,
    ThemeToggleButtonComponent,
    // NotificationDropdownComponent,
    UserDropdownComponent,
    FormsModule,
    RouterLink
],
  templateUrl: './app-header.component.html',
  styleUrl: './app-header.component.css'
})
export class AppHeaderComponent {
  isApplicationMenuOpen = false;
  readonly isMobileOpen$;
  searchTerm = '';
  books: Book[] = [];
  showDropdown = false;

  @ViewChild('searchInput') searchInput!: ElementRef<HTMLInputElement>;  
  private searchSubject = new Subject<string>();

  constructor(public sidebarService: SidebarService, private bookService: BookService) {
    this.isMobileOpen$ = this.sidebarService.isMobileOpen$;
    
    // Debounce pour limiter les appels HTTP
    this.searchSubject.pipe(debounceTime(300)).subscribe(term => {
      if (term.trim()) {
        this.bookService.searchBooks(term).subscribe({
          next: (res) => {
            this.books = res;
            this.showDropdown = res.length > 0;
          },
          error: (err) => console.error(err)
        });
      } else {
        this.books = [];
        this.showDropdown = false;
      }
    });
  }
  
  onSearchChange() {
    this.searchSubject.next(this.searchTerm);
  }
  

  selectBook(book: Book) {
    this.searchTerm = book.title;
    this.showDropdown = false;

      // this.router.navigate(['/books/']);
    // Ici tu peux router vers la page du livre si nécessaire
  }

  onSearch() {
    if (this.searchTerm.trim()) {
      this.bookService.searchBooks(this.searchTerm).subscribe({
        next: (res) => this.books = res,
        error: (err) => console.error(err)
      });
    } else {
      this.books = [];
    }
  }
    handleToggle() {
    if (window.innerWidth >= 1280) {
      this.sidebarService.toggleExpanded();
    } else {
      this.sidebarService.toggleMobileOpen();
    }
  }

  toggleApplicationMenu() {
    this.isApplicationMenuOpen = !this.isApplicationMenuOpen;
  }


  ngAfterViewInit() {
    document.addEventListener('keydown', this.handleKeyDown);
  }

  ngOnDestroy() {
    document.removeEventListener('keydown', this.handleKeyDown);
  }

  handleKeyDown = (event: KeyboardEvent) => {
    if ((event.metaKey || event.ctrlKey) && (event.key === 'q' || event.key === 'Q')) {
      event.preventDefault();
      this.searchInput?.nativeElement.focus();
    }
  };

}
