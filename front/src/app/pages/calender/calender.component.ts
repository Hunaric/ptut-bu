import { Component, OnInit, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FullCalendarComponent, FullCalendarModule } from '@fullcalendar/angular';


import { EventInput, CalendarOptions, DateSelectArg, EventClickArg } from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import { ModalComponent } from '../../shared/components/ui/modal/modal.component';
import { KeyValuePipe } from '@angular/common';
import { LoanService } from '../../services/loan.service';
import { LoanCalendar } from '../../interfaces/loan';
import { PageBreadcrumbComponent } from '../../components/common/page-breadcrumb/page-breadcrumb.component';


interface CalendarEvent extends EventInput {
  extendedProps: {
    calendar: string;
  };
}

@Component({
  selector: 'app-calender',
  imports: [
    FullCalendarModule,
    ModalComponent, 
    KeyValuePipe,
    FormsModule, 
    PageBreadcrumbComponent
  ],
  templateUrl: './calender.component.html',
  styleUrl: './calender.component.css'
})
export class CalenderComponent implements OnInit {

  @ViewChild('calendar') calendarComponent!: FullCalendarComponent;

  constructor(private loanService: LoanService) {}
async ngOnInit() {
  await this.loadLateLoans();

  this.calendarOptions = {
    ...this.calendarOptions,
    headerToolbar: {
      left: 'prev,next addEventButton',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    events: this.events
  };
}

async loadLateLoans() {
  const loans: LoanCalendar[] = await this.loanService.getLateLoans();

  const today = new Date();
  const warningDays = 7; // nombre de jours pour considérer “à rendre bientôt”

  const events: CalendarEvent[] = loans.map(loan => {
    const dueDate = new Date(loan.due_date);
    let calendarLevel = '';
    let titleSuffix = '';

    if (dueDate < today) {
      // en retard
      calendarLevel = 'Danger';
      titleSuffix = 'en retard';
    } else if (dueDate <= new Date(today.getTime() + warningDays * 24 * 60 * 60 * 1000)) {
      // à rendre bientôt
      calendarLevel = 'Warning';
      titleSuffix = 'à rendre bientôt';
    } else {
      calendarLevel = 'Success';
      titleSuffix = '';
    }

    return {
      id: loan.id.toString(),
      title: `${loan.book_title}${titleSuffix ? ' (' + titleSuffix + ')' : ''}`,
      start: dueDate.toISOString().split('T')[0],
      extendedProps: { calendar: calendarLevel }
    };
  });

  this.events = [...events];

  // trigger rerender du calendrier
  this.calendarOptions = {
    ...this.calendarOptions,
    events: [...this.events]
  };
}

    calendarOptions: CalendarOptions = {
      plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
      initialView: 'dayGridMonth',
      headerToolbar: {
        left: 'prev,next addEventButton',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
      },
      selectable: true,
      events: [],
      select: (info) => this.handleDateSelect(info),
      eventClick: (info) => this.handleEventClick(info),
      customButtons: {
        addEventButton: {
          text: 'Ajouter un evenement +',
          click: () => this.openModal()
        }
      },
      eventContent: (arg) => this.renderEventContent(arg)
    };
  
  events: CalendarEvent[] = [];
  selectedEvent: CalendarEvent | null = null;
  eventTitle = '';
  eventStartDate = '';
  eventEndDate = '';
  eventLevel = '';
  isOpen = false;

  calendarsEvents: Record<string, string> = {
    Danger: 'danger',
    Success: 'success',
    Primary: 'primary',
    Warning: 'warning'
  };




  handleDateSelect(selectInfo: DateSelectArg) {
    this.resetModalFields();
    this.eventStartDate = selectInfo.startStr;
    this.eventEndDate = selectInfo.endStr || selectInfo.startStr;
    this.openModal();
  }

  handleEventClick(clickInfo: EventClickArg) {
    const event = clickInfo.event as any;
    this.selectedEvent = {
      id: event.id,
      title: event.title,
      start: event.startStr,
      end: event.endStr,
      extendedProps: { calendar: event.extendedProps.calendar }
    };
    this.eventTitle = event.title;
    this.eventStartDate = event.startStr;
    this.eventEndDate = event.endStr || '';
    this.eventLevel = event.extendedProps.calendar;
    this.openModal();
  }

  handleAddOrUpdateEvent() {
    if (this.selectedEvent) {
      this.events = this.events.map(ev =>
        ev.id === this.selectedEvent!.id
          ? {
              ...ev,
              title: this.eventTitle,
              start: this.eventStartDate,
              end: this.eventEndDate,
              extendedProps: { calendar: this.eventLevel }
            }
          : ev
      );
    } else {
      const newEvent: CalendarEvent = {
        id: Date.now().toString(),
        title: this.eventTitle,
        start: this.eventStartDate,
        end: this.eventEndDate,
        allDay: true,
        extendedProps: { calendar: this.eventLevel }
      };
      this.events = [...this.events, newEvent];
    }
    this.calendarOptions.events = this.events;
    this.closeModal();
    this.resetModalFields();
  }

  resetModalFields() {
    this.eventTitle = '';
    this.eventStartDate = '';
    this.eventEndDate = '';
    this.eventLevel = '';
    this.selectedEvent = null;
  }

  openModal() {
    this.isOpen = true;
  }

  closeModal() {
    this.isOpen = false;
    this.resetModalFields();
  }

  renderEventContent(eventInfo: any) {
    const colorClass = `fc-bg-${eventInfo.event.extendedProps.calendar?.toLowerCase()}`;
    return {
      html: `
        <div class="event-fc-color flex fc-event-main ${colorClass} p-1 rounded-sm">
          <div class="fc-daygrid-event-dot"></div>
          <div class="fc-event-time">${eventInfo.timeText || ''}</div>
          <div class="fc-event-title">${eventInfo.event.title}</div>
        </div>
      `
    };
  }
}
