import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environment/environment';
import { Observable } from 'rxjs';
import { User } from '../interfaces/user';

export interface Permission {
  id: number;
  name: string;
  description?: string;
}

@Injectable({ providedIn: 'root' })
export class PermissionService {

  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  /** 🔹 Liste des permissions */
  getPermissions(): Observable<Permission[]> {
    return this.http.get<Permission[]>(`${this.baseUrl}/permissions`);
  }

  /** 🔹 Recherche user par username ou email */
  searchUser(identifier: string): Observable<User> {
    return this.http.get<User>(
      `${this.baseUrl}/users/by-identifier/${identifier}`
    );
  }

  /** 🔹 Assigner une permission */
  assignPermission(userId: string, permissionId: number): Observable<any> {
    return this.http.post(
      `${this.baseUrl}/users/${userId}/permissions/${permissionId}`,
      {}
    );
  }

  /** 🔹 Retirer une permission */
  removePermission(userId: string, permissionId: number): Observable<any> {
    return this.http.delete(
      `${this.baseUrl}/users/${userId}/permissions/${permissionId}`
    );
  }
}
