import { Routes } from '@angular/router';
import { AppLayoutComponent } from './shared/layout/app-layout/app-layout.component';

export const routes: Routes = [
    // Page d'accueil
    {
        path: '',
        component: AppLayoutComponent,
        children: [
            
        ],
    }
];
