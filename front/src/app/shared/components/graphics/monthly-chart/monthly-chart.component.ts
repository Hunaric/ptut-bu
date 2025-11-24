import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-monthly-chart',
  imports: [
    CommonModule,
    NgApexchartsModule,
    DropdownComponent,
    DropdownItemComponent,
  ],
  templateUrl: './monthly-chart.component.html',
  styleUrl: './monthly-chart.component.css'
})
export class MonthlyChartComponent {

}
