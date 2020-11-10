import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.scss'],
})
export class LoginFormComponent implements OnInit {
  hasLoginError = false;

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {}

  login(username: string, password: string) {
    this.authService.login(username, password).subscribe((res) => {
      this.router.navigateByUrl('/dashboard');
    });
  }
}
