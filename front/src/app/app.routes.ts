import { Routes } from '@angular/router';
import { AppLayoutComponent } from './shared/layout/app-layout/app-layout.component';
import { DashboardComponent } from './admin/dashboard/dashboard.component';
import { CalenderComponent } from './pages/calender/calender.component';
import { BookComponent } from './admin/book/book.component';

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
                title: 'Dashboard',
                    
            },
            {
                path:'calendar',
                component:CalenderComponent,
                title:'Angular Calender | TailAdmin - Angular Admin Dashboard Template'
            },
            {
                path:'books',
                component:BookComponent,
                title:'Angular Calender | TailAdmin - Angular Admin Dashboard Template'
            },
            
        ],
    }
];
