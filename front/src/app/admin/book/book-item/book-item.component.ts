import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-book-item',
  imports: [
  ],
  templateUrl: './book-item.component.html',
  styleUrl: './book-item.component.css',
})
export class BookItemComponent {
  
  @Input() imageUrl?: string;

  fallbackUrl = '/images/grid-image/image-03.png';

  get src(): string {
    return this.imageUrl?.trim() || this.fallbackUrl;
  }

  onImageError(event: Event) {
    this.setFallback(event);
  }

  onImageLoad(event: Event) {
    const img = event.target as HTMLImageElement;

    // OpenLibrary retourne parfois une image 1x1 vide
    if (img.naturalWidth <= 1 || img.naturalHeight <= 1) {
      this.setFallback(event);
    }
  }

  private setFallback(event: Event) {
    const img = event.target as HTMLImageElement;

    if (img.src !== this.fallbackUrl) {
      img.src = this.fallbackUrl;
    }
  }

}
