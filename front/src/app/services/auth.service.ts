import { Injectable } from '@angular/core';
import { environment } from '../../environment/environment';
// import { Client } from '../interface/client';
import { firstValueFrom, Subject } from 'rxjs';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MyPermissions } from '../interfaces/permission';
import { Me } from '../interfaces/user';

@Injectable({providedIn: 'root'})
export class AuthService {
  private apiUrl = environment.apiUrl;
  sessionExpired$ = new Subject<void>();

  constructor(private router: Router, private http: HttpClient) { 
    this.sessionExpired$.subscribe(() => this.logout());
  }

  get accessToken(): string | null {
    return localStorage.getItem('access_token');
  }
  

  getPermissions(): string[] {
    const permJson = localStorage.getItem('permissions');
    return permJson ? JSON.parse(permJson) : [];
  }


  logout(): void {
    localStorage.clear();
    // console.log("Déconnexion effectuée");
    this.router.navigate(['/signin']);
  }

  notifySessionExpired(): void {
    this.logout();
  }
  
  async onLogedIn(identifier: string, password: string): Promise<any> {
    const url = `${this.apiUrl}/auth/login`;
    const options = {
      method: 'POST',
      headers: {'Content-Type': 'application/json', Accept: 'application/json'},
      body: '{"identifier":"'+identifier+'","password":"'+password+'"}'
    };
    
    try {
      const response = await fetch(url, options);
      console.log('OK');
      
      const data = await response.json();
      
      if (response.ok && data.access_token) {
        localStorage.setItem('access_token', data.access_token);
      }
      // // console.log(data);
      return data ?? [];
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
  

async getMe(): Promise<Me> {
  const token = localStorage.getItem('access_token');
  if (!token) throw new Error('No access token');

  const res = await fetch(`${this.apiUrl}/auth/me`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/json'
    }
  });
  
  if (!res.ok) throw new Error('Impossible de récupérer les infos utilisateur');
  return res.json();
}

}