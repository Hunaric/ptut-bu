import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { ButtonComponent } from '../button/button.component';
import { TruncatePipe } from '../../../pipe/truncate.pipe';

@Component({
  selector: 'app-card',
  imports: [CommonModule, ButtonComponent, TruncatePipe],
  templateUrl: './card.component.html',
  styleUrl: './card.component.css',
})
export class CardComponent {

  @Input() title!: string;
  @Input() desc?: string = '';
  @Input() className: string = '';
  
}
