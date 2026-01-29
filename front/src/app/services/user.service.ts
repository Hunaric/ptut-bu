import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environment/environment';
import { firstValueFrom } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class UserService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  private get headers() {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    });
  }

  getUserById(userId: string) {
    return firstValueFrom(
      this.http.get(`${this.apiUrl}/users/${userId}`, { headers: this.headers })
    );
  }

  updateUser(userId: string, data: any) {
    return firstValueFrom(
      this.http.put(`${this.apiUrl}/users/${userId}`, data, { headers: this.headers })
    );
  }

  updateAccount(userId: string, data: any) {
    return firstValueFrom(
      this.http.put(`${this.apiUrl}/users/${userId}/account`, data, { headers: this.headers })
    );
  }
}
