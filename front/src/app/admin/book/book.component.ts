import { Component } from '@angular/core';
import { BookItemComponent } from './book-item/book-item.component';
import { PageBreadcrumbComponent } from '../../components/common/page-breadcrumb/page-breadcrumb.component';
import { CardComponent } from '../../shared/components/ui/card/card.component';

@Component({
  selector: 'app-book',
  imports: [
    PageBreadcrumbComponent,
    CardComponent,
    BookItemComponent
  ],
  templateUrl: './book.component.html',
  styleUrl: './book.component.css',
})
export class BookComponent {

}
