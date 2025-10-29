import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { SidebarService } from '../../services/sidebar.service';

@Component({
  selector: 'app-app-backdrop',
  imports: [
    CommonModule
  ],
  templateUrl: './app-backdrop.component.html',
  styleUrl: './app-backdrop.component.css'
})
export class AppBackdropComponent {
  readonly isMobileOpen$;

  constructor(private sidebarService: SidebarService) {
    this.isMobileOpen$ = this.sidebarService.isMobileOpen$;
  }

  closeSidebar() {
    this.sidebarService.setMobileOpen(false);
  }

}
