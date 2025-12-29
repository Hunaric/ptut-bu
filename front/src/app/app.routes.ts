import { Routes } from '@angular/router';
import { AppLayoutComponent } from './shared/layout/app-layout/app-layout.component';
import { DashboardComponent } from './admin/dashboard/dashboard.component';
import { CalenderComponent } from './pages/calender/calender.component';
import { BookComponent } from './admin/book/book.component';
import { SignInComponent } from './pages/auth-pages/sign-in/sign-in.component';
import { SignUpComponent } from './pages/auth-pages/sign-up/sign-up.component';
import { NotFoundComponent } from './pages/other-pages/not-found/not-found.component';
import { authGuard } from './guards/auth.guard';
import { CrudBookComponent } from './pages/crud-book/crud-book.component';
import { DetailBookComponent } from './pages/detail-book/detail-book.component';
import { MyLoansComponent } from './pages/my-loans/my-loans.component';

export const routes: Routes = [
    // Page d'accueil
    {
        path: '',
        component: AppLayoutComponent,
        canActivate: [authGuard],
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
                title:'Calendrier des retours'
            },
            {
                path:'books',
                component:BookComponent,
                title:'Les livres'
            },
            {
                path:'crud-books',
                component:CrudBookComponent,
                title:'Gestion des livres'
            },
            {
                path:'crud-books/:id',
                component:CrudBookComponent,
                title:'Modifier un livre'
            },
            {
                path:'detail-books/:id',
                component:DetailBookComponent,
                title:'Detail du livre'
            },
            {
                path:'my-loans',
                component:MyLoansComponent,
                title:'Mes emprunts'
            },
            
        ],
    }, 
  // auth pages
  {
    path:'signin',
    component:SignInComponent,
    title:'Sign In'
  },
  {
    path:'signup',
    component:SignUpComponent,
    title:'Sign Up'
  },
  // error pages
  {
    path:'**',
    component:NotFoundComponent,
    title:'NotFound'
  },
];
