import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { environment } from '../../environment/environment';
import { DashboardStats } from '../interfaces/dashboard-stats';

@Injectable({
  providedIn: 'root'
})
export class StatsService {

  private apiUrl = `${environment.apiUrl}/stats/user/dashboard`;

  get accessToken(): string | null {
    return localStorage.getItem('access_token');
  }
  

  constructor(private http: HttpClient) {}
  
  async getDashboardStats(
  year: number = new Date().getFullYear()
): Promise<DashboardStats> {

  const token = this.accessToken;

  return firstValueFrom(
    this.http.get<DashboardStats>(
      `${this.apiUrl}?year=${year}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
  );
}


}
