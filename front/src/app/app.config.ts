  import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
  import { provideRouter } from '@angular/router';
  import { HTTP_INTERCEPTORS, provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
  import { routes } from './app.routes';
import { AuthInterceptor } from './interceptor/auth.interceptor';

  export const appConfig: ApplicationConfig = {
    providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes), provideHttpClient(), provideHttpClient(withInterceptorsFromDi()),  // Active les interceptors DI
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }]
  };
