// book.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

import { environment } from '../../environment/environment';
import { PaginatedResponse } from '../interfaces/paginated-response';
import { Book } from '../interfaces/book';

@Injectable({
  providedIn: 'root',
})
export class BookService {

  private apiUrl = `${environment.apiUrl}/books`;
  private accessToken: string | null = null;

  constructor(private http: HttpClient) {
    this.accessToken = localStorage.getItem('access_token');
  }

  private getAuthHeaders() {
    return {
      Authorization: `Bearer ${this.accessToken}`,
      Accept: 'application/json',
    };
  }

  /**
   * 📚 Récupérer tous les livres
   * GET /books
   */
  async getBooks(skip = 0, limit = 100): Promise<Book[]> {
    const url = `${this.apiUrl}`;

    try {
      const data = await firstValueFrom(
        this.http.get<Book[]>(url, {
          headers: this.getAuthHeaders(),
          params: {
            skip,
            limit,
          },
        })
      );
      return data;
    } catch (error) {
      console.error('Erreur lors de la récupération des livres', error);
      throw error;
    }
  }

  /**
   * 📖 Récupérer un livre par ID
   * GET /books/{id}
   */
  async getBookById(id: number): Promise<Book> {
    const url = `${this.apiUrl}/${id}`;

    try {
      const data = await firstValueFrom(
        this.http.get<Book>(url, {
          headers: this.getAuthHeaders(),
        })
      );
      return data;
    } catch (error) {
      console.error(`Erreur lors de la récupération du livre ${id}`, error);
      throw error;
    }
  }

  /**
   * 🔍 Recherche avancée paginée
   * GET /books/advanced
   */
  async getBooksAdvanced(
    page = 1,
    size = 10,
    categoryId?: number,
    tagIds?: number[]
  ): Promise<PaginatedResponse<Book>> {

    const url = `${this.apiUrl}/advanced`;
    console.log(url);
    
    let params = new HttpParams()
      .set('page', page)
      .set('size', size);

    if (categoryId) {
      params = params.set('category_id', categoryId);
    }

    if (tagIds && tagIds.length) {
      tagIds.forEach(id => {
        params = params.append('tag_ids', id);
      });
    }

    try {
      const data = await firstValueFrom(
        this.http.get<PaginatedResponse<Book>>(url, {
          headers: this.getAuthHeaders(),
          params,
        })
      );
      return data;
    } catch (error) {
      console.error('Erreur lors de la recherche avancée des livres', error);
      throw error;
    }
  }

  /**
   * ➕ Créer un livre
   * POST /books
   */
  async createBook(book: Partial<Book>): Promise<Book> {
    const url = `${this.apiUrl}`;

    try {
      const data = await firstValueFrom(
        this.http.post<Book>(url, book, {
          headers: this.getAuthHeaders(),
        })
      );
      return data;
    } catch (error) {
      console.error('Erreur lors de la création du livre', error);
      throw error;
    }
  }

  /**
   * ✏️ Mettre à jour un livre
   * PUT /books/{id}
   */
  async updateBook(id: number, book: Partial<Book>): Promise<Book> {
    const url = `${this.apiUrl}/${id}`;

    try {
      const data = await firstValueFrom(
        this.http.put<Book>(url, book, {
          headers: this.getAuthHeaders(),
        })
      );
      return data;
    } catch (error) {
      console.error(`Erreur lors de la mise à jour du livre ${id}`, error);
      throw error;
    }
  }

  /**
   * 🗑 Supprimer un livre
   * DELETE /books/{id}
   */
  async deleteBook(id: number): Promise<void> {
    const url = `${this.apiUrl}/${id}`;

    try {
      await firstValueFrom(
        this.http.delete<void>(url, {
          headers: this.getAuthHeaders(),
        })
      );
    } catch (error) {
      console.error(`Erreur lors de la suppression du livre ${id}`, error);
      throw error;
    }
  }
}
