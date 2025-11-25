import { Component } from '@angular/core';
import { GridShapeComponent } from '../../components/common/grid-shape/grid-shape.component';
import { ThemeToggleTwoComponent } from '../../components/common/theme-toggle-two/theme-toggle-two.component';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-auth-page-layout',
  imports: [
    GridShapeComponent,
    ThemeToggleTwoComponent,
    RouterModule,
  ],
  templateUrl: './auth-page-layout.component.html',
  styleUrl: './auth-page-layout.component.css',
})
export class AuthPageLayoutComponent {

}
