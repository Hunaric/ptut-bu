import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { UserService } from '../../services/user.service';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';
import { User } from '../../interfaces/user';

@Component({
  selector: 'app-user',
  imports: [
    ReactiveFormsModule, 
    CommonModule, 
  ],
  templateUrl: './user.component.html',
  styleUrl: './user.component.css',
})
export class UserComponent {

  user!: User;
  userForm!: FormGroup;
  accountForm!: FormGroup;
  userId!: string;
  loading = false;
  successMsg = '';
  errorMsg = '';

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private authService: AuthService
  ) {}

  
async ngOnInit() {

  
this.userForm = this.fb.group({
  email: [''],
  username: [''],
  role: ['']
});


    this.accountForm = this.fb.group({
      nom: [''],
      prenom: [''],
      sexe: [''],
      telephone: [''],
      pays: [''],
      ville: [''],
      rue: ['']
    });

  try {
    // 1️⃣ récupérer le "me" de la session
    const me = await this.authService.getMe2();

    const identifier = me.email ?? me.username;

    // 2️⃣ récupérer l'utilisateur complet via /users/by-identifier/{identifier}
    this.user = await this.authService.getUserByIdentifier(identifier);
    console.log("user:", this.user);
    this.userId = this.user.id;
    
    // 3️⃣ initialiser les forms
    this.userForm = this.fb.group({
      email: [this.user.email],
      username: [this.user.username],
      role: [this.user.role?.name ?? '']
    });

    this.accountForm = this.fb.group({
      nom: [this.user.account?.nom ?? ''],
      prenom: [this.user.account?.prenom ?? ''],
      sexe: [this.user.account?.sexe ?? ''],
      telephone: [this.user.account?.telephone ?? ''],
      pays: [this.user.account?.pays ?? ''],
      ville: [this.user.account?.ville ?? ''],
      rue: [this.user.account?.rue ?? '']
    });

  } catch (err) {
    console.error("Erreur chargement utilisateur :", err);
    this.errorMsg = 'Impossible de charger l’utilisateur';
  }
}


  async loadUser() {
    try {
      const user: any = await this.userService.getUserById(this.userId);

      this.userForm.patchValue({
        email: user.email,
        username: user.username,
        role: user.role?.name
      });

      if (user.account) {
        this.accountForm.patchValue(user.account);
      }
    } catch (err) {
      this.errorMsg = 'Erreur chargement utilisateur';
    }
  }

  async saveUser() {
  this.loading = true;
  try {
    // Créer un payload complet pour l'API
    const payload = {
      email: this.userForm.value.email ?? '',
      username: this.userForm.value.username ?? '',
    };

    console.log('Payload utilisateur envoyé :', payload);

    await this.userService.updateUser(this.userId, payload);
    this.successMsg = 'Utilisateur mis à jour avec succès';
    this.errorMsg = '';
  } catch (err: any) {
    console.error(err);
    this.errorMsg = 'Erreur mise à jour utilisateur';
    this.successMsg = '';
  } finally {
    this.loading = false;
  }
}

  
async saveAccount() {
  this.loading = true;
  try {
    // Créer un objet complet pour l'API
    const payload = {
      sexe: this.accountForm.value.sexe ?? '',
      nom: this.accountForm.value.nom ?? '',
      prenom: this.accountForm.value.prenom ?? '',
      etablissement: this.accountForm.value.etablissement ?? '',
      numero: this.accountForm.value.numero ?? '',
      rue: this.accountForm.value.rue ?? '',
      boite_postale: this.accountForm.value.boite_postale ?? '',
      code_postal: this.accountForm.value.code_postal ?? '',
      ville: this.accountForm.value.ville ?? '',
      codex_ville: this.accountForm.value.codex_ville ?? '',
      pays: this.accountForm.value.pays ?? '',
      telephone: this.accountForm.value.telephone ?? ''
    };

    console.log('Payload envoyé :', payload);

    await this.userService.updateAccount(this.userId, payload);
    this.successMsg = 'Compte mis à jour avec succès';
    this.errorMsg = '';
  } catch (err: any) {
    console.error(err);
    this.errorMsg = 'Erreur mise à jour compte';
    this.successMsg = '';
  } finally {
    this.loading = false;
  }
}

}
