import { Injectable } from '@angular/core';
import { environment } from '../../environment/environment';
// import { Client } from '../interface/client';
import { firstValueFrom, Subject } from 'rxjs';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({providedIn: 'root'})
export class AuthService {
  private apiUrl = environment.apiUrl;
  sessionExpired$ = new Subject<void>();

  constructor(private router: Router, private http: HttpClient) { 
    this.sessionExpired$.subscribe(() => this.logout());
  }

  get accessToken(): string | null {
    return localStorage.getItem('accessToken');
  }
  
  getToken(): string | null {
    return localStorage.getItem('access_token');
  }
  

  logout(): void {
    localStorage.clear();
    // console.log("Déconnexion effectuée");
    this.router.navigate(['/auth']);
  }

  notifySessionExpired(): void {
    // alert('Sitzung abgelaufen. Bitte melden Sie sich erneut an.');
    this.logout();
  }
  
  async onLogedIn(email: string, password: string): Promise<any> {
    const url = `${this.apiUrl}/client/login`;
    const options = {
      method: 'POST',
      headers: {'Content-Type': 'application/json', Accept: 'application/json'},
      body: '{"email":"'+email+'","password":"'+password+'"}'
    };

    try {
      const response = await fetch(url, options);
      const data = await response.json();

    if (response.ok && data.accessToken) {
      localStorage.setItem('accessToken', data.accessToken);
    }
      // // console.log(data);
      return data ?? [];
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
  
  async registration(data: any): Promise<any> {
    const url = `${this.apiUrl}/clients/registration`;

    const options = {
      method: 'POST',
      headers: {'Content-Type': 'application/json', Accept: 'application/json'},
      body: JSON.stringify(data)
    }
    ;

    try {
      
      const response = await fetch(url, options);
      const data = await response.json();
      console.log("Données envoyées :", data);
      // // console.log(data);
      return data ?? [];
    } catch (error) {
      console.error(error);
      throw error;
    }
  }


  // Récupérer l'utilisateur courant avec HttpClient
  // async readCurrentUser(): Promise<Client> {
  //   const url = `${this.apiUrl}/clients/me`;
  //   try {
  //     const client = await firstValueFrom(
  //       this.http.get<Client>(url, {
  //         headers: new HttpHeaders({
  //           'Accept': 'application/json',
  //           'Authorization': `Bearer ${this.accessToken}`
  //         })
  //       })
  //     );
  //     return client;
  //   } catch (error) {
  //     console.error(error);
  //     throw error;
  //   }
  // }

  
  forgotPassword(email: string) {
    return this.http.post(`${this.apiUrl}/clients/forgot-password`, { email });
  }

  resetPassword(token: string, newPassword: string) {
    return this.http.post(`${this.apiUrl}/clients/reset-password`, {
      token,
      new_password: newPassword
    });
  }
}