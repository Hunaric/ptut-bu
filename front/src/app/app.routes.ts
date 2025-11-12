import { Routes } from '@angular/router';
import { AppLayoutComponent } from './shared/layout/app-layout/app-layout.component';
import { DashboardComponent } from './admin/dashboard/dashboard.component';

export const routes: Routes = [
    // Page d'accueil
    {
        path: '',
        component: AppLayoutComponent,
        children: [
            {
                path: '',
                component: DashboardComponent,
                pathMatch: 'full',
                title: 'Dashboard'
            },
            
        ],
    }
];
