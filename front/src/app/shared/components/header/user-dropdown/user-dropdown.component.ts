import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { DropdownComponent } from '../../ui/dropdown/dropdown.component';
import { DropdownItemTwoComponent } from '../../ui/dropdown/dropdown-item/dropdown-item.component-two';
import { AuthService } from '../../../../services/auth.service';
import { Me } from '../../../../interfaces/user';

@Component({
  selector: 'app-user-dropdown',
  imports: [CommonModule, RouterModule, DropdownComponent, DropdownItemTwoComponent],
  templateUrl: './user-dropdown.component.html',
  styleUrl: './user-dropdown.component.css',
})
export class UserDropdownComponent {
  me: Me | null = null;
  isOpen = false;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.loadUser();
  }

  async loadUser() {
    try {
      this.me = await this.authService.getMe();
    } catch (error) {
      console.error('Impossible de récupérer l’utilisateur', error);
    }
  }

  toggleDropdown() {
    this.isOpen = !this.isOpen;
  }

  closeDropdown() {
    this.isOpen = false;
  }
}
