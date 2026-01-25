import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { LabelComponent } from '../../form/label/label.component';
import { CheckboxComponent } from '../../form/input/checkbox.component';
import { InputFieldComponent } from '../../form/input/input-field.component';
import { Router, RouterModule } from '@angular/router';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../../../services/auth.service';


@Component({
  selector: 'app-signup-form',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    LabelComponent,
    InputFieldComponent,
    RouterModule,
    FormsModule,
    CheckboxComponent
  ],
  templateUrl: './signup-form.component.html',
  styles: ``
})
export class SignupFormComponent {

  signupForm = new FormGroup({
    prenom: new FormControl('', [Validators.required]),
    nom: new FormControl('', [Validators.required]),
    username: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, Validators.minLength(8)]),
    sexe: new FormControl('', [Validators.required]),
    etablissement: new FormControl('', [Validators.required]),
    numero: new FormControl('', [Validators.required]),
    rue: new FormControl('', [Validators.required]),
    boite_postale: new FormControl(''),
    code_postal: new FormControl('', [Validators.required]),
    ville: new FormControl('', [Validators.required]),
    codex_ville: new FormControl(''),
    pays: new FormControl('', [Validators.required]),
    telephone: new FormControl('', [Validators.required]),
  });

  showPassword = false;
  isChecked = false;
  error: string | null = null;

  constructor(private authService: AuthService, private router: Router) {}

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  async onSignup(event?: Event) {
    if (event) event.preventDefault();

    if (this.signupForm.invalid) {
      this.error = 'Veuillez remplir correctement tous les champs obligatoires';
      return;
    }

    try {
      const formData = this.signupForm.value;
      const res = await this.authService.signup(formData);

      if (res && res.success) {
        this.router.navigate(['/login']);
      } else {
        this.error = res.detail || 'Erreur lors de l’inscription';
      }
    } catch (err: any) {
      console.error('Erreur lors de l’inscription :', err);
      this.error = err?.error?.detail || 'Erreur serveur';
    }
  }
}
