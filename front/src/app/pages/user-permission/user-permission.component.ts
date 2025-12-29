import { Component, OnInit } from '@angular/core';
import { PermissionService, Permission } from '../../services/permission.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { User } from '../../interfaces/user';

@Component({
  selector: 'app-user-permission',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user-permission.component.html',
})
export class UserPermissionComponent implements OnInit {

  query = '';
  user: User | null = null;

  permissions: Permission[] = [];
  selectedPermissionId?: number;

  loading = false;
  message = '';
  error = '';

  constructor(private permissionService: PermissionService) {}
    
  hasPermission(permissionId: number): boolean {
    return !!this.user?.permissions?.some(p => p.id === permissionId);
  }

  ngOnInit() {
    this.permissionService.getPermissions().subscribe(p => this.permissions = p);
  }

  searchUser() {
    this.error = '';

    this.permissionService.searchUser(this.query).subscribe({
      next: (user) => this.user = user,
      error: () => this.error = 'Utilisateur introuvable'
    });
  }

assignPermission() {
  if (!this.user || !this.selectedPermissionId) return;

  this.permissionService
    .assignPermission(this.user.id, this.selectedPermissionId)
    .subscribe({
      next: () => {
        this.message = 'Permission assignée avec succès';
        this.searchUser(); // 🔄 refresh
      },
      error: err => {
        this.error = err.error?.detail ?? 'Erreur lors de l’assignation';
      }
    });
}

removePermission() {
  if (!this.user || !this.selectedPermissionId) return;

  this.permissionService
    .removePermission(this.user.id, this.selectedPermissionId)
    .subscribe({
      next: () => {
        this.message = 'Permission retirée';
        this.searchUser(); // 🔄 refresh
      }
    });
}

}
