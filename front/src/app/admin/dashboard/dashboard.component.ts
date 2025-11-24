import { Component } from '@angular/core';
import { FullCalendarModule } from '@fullcalendar/angular';
import { CalendarOptions } from '@fullcalendar/core/index.js';
import { MonthlyChartComponent } from '../../shared/components/graphics/monthly-chart/monthly-chart.component';
import { MonthlyTargetComponent } from '../../shared/components/graphics/monthly-target/monthly-target.component';
import { MetricsComponent } from '../../shared/components/graphics/metrics/metrics.component';

@Component({
  selector: 'app-dashboard',
  imports: [
    MonthlyChartComponent,
    MonthlyTargetComponent,
    MetricsComponent,
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  calendarOptions!: CalendarOptions;

}
