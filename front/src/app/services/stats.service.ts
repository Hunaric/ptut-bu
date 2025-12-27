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

  async getDashboardStats(): Promise<DashboardStats> {
    return firstValueFrom(
    this.http.get<DashboardStats>(this.apiUrl)
  );
  }
}
