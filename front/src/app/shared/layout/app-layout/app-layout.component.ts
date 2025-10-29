import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AppHeaderComponent } from '../app-header/app-header.component';
import { AppSidebarComponent } from '../app-sidebar/app-sidebar.component';
import { AppBackdropComponent } from "../app-backdrop/app-backdrop.component";
import { AppFooterComponent } from '../app-footer/app-footer.component';

@Component({
  selector: 'app-app-layout',
  imports: [
    RouterOutlet,
    AppHeaderComponent,
    AppSidebarComponent,
    AppBackdropComponent, 
    AppFooterComponent
],
  templateUrl: './app-layout.component.html',
  styleUrl: './app-layout.component.css'
})
export class AppLayoutComponent {

}
