import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { environment } from '../../environment/environment';
import { LoanCalendar } from '../interfaces/loan';



@Injectable({
  providedIn: 'root'
})
export class LoanService {
  private apiUrl = `${environment.apiUrl}/loans/late`;

  constructor(private http: HttpClient) {}

  async getLateLoans(): Promise<LoanCalendar[]> {
    return firstValueFrom(this.http.get<LoanCalendar[]>(this.apiUrl));
  }
}
