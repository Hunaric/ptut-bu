import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { InputFieldComponent } from '../../form/input/input-field.component';
import { LabelComponent } from '../../form/label/label.component';
import { ButtonComponent } from '../../ui/button/button.component';
import { AuthService } from '../../../../services/auth.service';

@Component({
  selector: 'app-signin-form',
  imports: [
    CommonModule,
    LabelComponent,
    ButtonComponent,
    InputFieldComponent,
    RouterModule,
    FormsModule,
    ReactiveFormsModule
  ],
  templateUrl: './signin-form.component.html',
  styleUrl: './signin-form.component.css',
})
export class SigninFormComponent {

  constructor(private authService: AuthService, private router: Router) {}

  showPassword = false;
  isChecked = false;
  error: string | null = null;

  identifier = '';
  password = '';

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }


  loginForm = new FormGroup({
    identifier: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required]),
  })

  async onLogedIn(event?: Event) {
    if(event) {
      event.preventDefault(); 
    }
    if(!this.loginForm.value.identifier || !this.loginForm.value.password) {
      console.error('Error');
      return
    } else {
      try {
        var identifier = this.loginForm.value.identifier;
        var password = this.loginForm.value.password;

        const res = await this.authService.onLogedIn(identifier, password);
        
        if (res && res.access_token) {
          localStorage.setItem('access_token', res.access_token);
          // console.log(res);
          
          const me = await this.authService.getMe();
          localStorage.setItem('permissions', JSON.stringify(me.permissions));
          // console.log('info :', me);
          
          
          // Navigation uniquement en cas de succès
          this.router.navigate(['']).then(success => {
            if (success) {
              // // console.log('Navigation réussie vers home');
              window.location.reload();
            } else {
              console.error('Échec de navigation');
            }
          });
        } else {
          console.error('Authentification échouée :', res.detail || 'Réponse invalide');
          this.error = res.detail;
        }
        
      } catch (error) {
        console.error('Erreur lors de la requête :', error);
      }
    }
    
  }

}
