import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { environment } from '../../environment/environment';
import { DashboardStats } from '../interfaces/dashboard-stats';

@Injectable({
  providedIn: 'root'
})
export class StatsService {

  private apiUrl = `${environment.apiUrl}/stats/dashboard`;

  constructor(private http: HttpClient) {}
async getDashboardStats(year: number = new Date().getFullYear()): Promise<any> {
  return firstValueFrom(this.http.get(`${this.apiUrl}?year=${year}`));
}

}
