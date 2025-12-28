import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { ButtonComponent } from '../button/button.component';
import { TruncatePipe } from '../../../pipe/truncate.pipe';
import { RouterLink } from "@angular/router";

@Component({
  selector: 'app-card',
  imports: [CommonModule, ButtonComponent, TruncatePipe, RouterLink],
  templateUrl: './card.component.html',
  styleUrl: './card.component.css',
})
export class CardComponent {

  @Input() bookId!: number;
  @Input() title!: string;
  @Input() desc?: string = '';
  @Input() className: string = '';
  
}
