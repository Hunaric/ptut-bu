import { Component, OnInit } from '@angular/core';
import { FullCalendarModule } from '@fullcalendar/angular';
import { CalendarOptions } from '@fullcalendar/core/index.js';
import { MonthlyChartComponent } from '../../shared/components/graphics/monthly-chart/monthly-chart.component';
import { MonthlyTargetComponent } from '../../shared/components/graphics/monthly-target/monthly-target.component';
import { MetricsComponent } from '../../shared/components/graphics/metrics/metrics.component';
import { DashboardStats } from '../../interfaces/dashboard-stats';
import { StatsService } from '../../services/stats.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  imports: [
    MonthlyChartComponent,
    MonthlyTargetComponent,
    MetricsComponent,
    CommonModule
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit{
  calendarOptions!: CalendarOptions;

  stats!: DashboardStats;

  constructor(private statsService: StatsService) {}

async ngOnInit() {
  this.stats = await this.statsService.getDashboardStats();
}


}
