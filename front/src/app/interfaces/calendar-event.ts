// calendar-event.model.ts
export type CalendarLevel =
  | 'primary'
  | 'success'
  | 'warning'
  | 'danger';

export type CalendarEventType =
  | 'custom'
  | 'loan';

export interface CalendarEvent {
  id: number;
  title: string;

  start: string;   // ISO date
  end?: string;

  level: CalendarLevel;
  type: CalendarEventType;
}
