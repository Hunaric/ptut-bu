import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { environment } from '../../environment/environment';
import { Loan, LoanCalendar } from '../interfaces/loan';
import { BorrowedBook } from '../interfaces/book';

@Injectable({
  providedIn: 'root'
})
export class LoanService {
  private apiUrl = environment.apiUrl;
  private accessToken: string | null = null;

  constructor(private http: HttpClient) {
    this.accessToken = localStorage.getItem('access_token');
    // console.log('[LoanService] Access token:', this.accessToken);
  }

  async createLoan(bookId: number): Promise<Loan> {
    try {
      const data = { book_id: bookId };
      const loan = await firstValueFrom(
        this.http.post<Loan>(`${this.apiUrl}/loans/`, data, {
          withCredentials: true, // si nécessaire pour token/session
        })
      );
      return loan;
    } catch (error) {
      console.error('Erreur lors de la création de l’emprunt', error);
      throw error;
    }
  }

  private getAuthHeaders(): HttpHeaders {
    return new HttpHeaders({
      Authorization: `Bearer ${this.accessToken || ''}`,
      Accept: 'application/json',
      'Content-Type': 'application/json'
    });
  }

  /** Récupère les prêts en retard */
  async getLateLoans(skip = 0, limit = 100): Promise<LoanCalendar[]> {
    const url = `${this.apiUrl}/loans/late`;
    try {
      const data = await firstValueFrom(
        this.http.get<LoanCalendar[]>(url, {
          headers: this.getAuthHeaders(),
          params: { skip, limit }
        })
      );
      // console.log('[LoanService] Late loans:', data);
      return data;
    } catch (error) {
      console.error('[LoanService] Erreur lors de la récupération des prêts en retard', error);
      throw error;
    }
  }

  /** Récupère les livres empruntés par l'utilisateur (non retournés) */
  async getMyLoans(skip = 0, limit = 100): Promise<BorrowedBook[]> {
    const url = `${this.apiUrl}/loans/me/borrowed`;
    try {
      const data = await firstValueFrom(
        this.http.get<BorrowedBook[]>(url, {
          headers: this.getAuthHeaders(),
          params: { skip, limit }
        })
      );
      // console.log('[LoanService] Mes emprunts:', data);
      return data;
    } catch (error) {
      console.error('[LoanService] Erreur lors de la récupération de mes emprunts', error);
      throw error;
    }
  }
}
