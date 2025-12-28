import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { Router, UrlTree } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { environment } from '../../environment/environment';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const http = inject(HttpClient);

  const token = localStorage.getItem('access_token');

  if (!token) {
    return router.parseUrl('/signin');
  }

  return http.get<{ valid: boolean }>(`${environment.apiUrl}/token/verify-token`, {
    headers: { Authorization: `Bearer ${token}` }
  }).pipe(
    map(res => {
      if (res.valid) return true;
      return router.parseUrl('/signin'); // redirection si token invalide
    }),
    catchError(err => of(router.parseUrl('/signin'))) // redirection si erreur réseau ou token invalide
  );
};
