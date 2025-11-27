import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-book-item',
  imports: [
  ],
  templateUrl: './book-item.component.html',
  styleUrl: './book-item.component.css',
})
export class BookItemComponent {
  @Input() imageUrl?: string;            // url reçue du parent
  fallbackUrl = '/images/grid-image/image-03.png';

  onImageError(event: Event) {
    const img = event.target as HTMLImageElement;
    img.src = this.fallbackUrl;
  }

}
