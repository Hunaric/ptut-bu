import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);

  const tokenAccess = localStorage.getItem('accessToken');

  if (tokenAccess) {
    return true;
  } else {
    router.navigate(['/signin']);
    return false;
  }
};
