import { Component } from '@angular/core';
import { FullCalendarModule } from '@fullcalendar/angular';
import { CalendarOptions } from '@fullcalendar/core/index.js';
import { CalenderComponent } from '../../pages/calender/calender.component';

@Component({
  selector: 'app-dashboard',
  imports: [
    CalenderComponent
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  calendarOptions!: CalendarOptions;

}
