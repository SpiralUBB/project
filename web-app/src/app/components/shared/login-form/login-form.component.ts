import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.scss'],
})
export class LoginFormComponent implements OnInit {
  hasLoginError = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private dialogRef: MatDialogRef<LoginFormComponent>
  ) {}

  ngOnInit(): void {}

  login(username: string, password: string): void {
    this.authService.login(username, password).subscribe((res) => {
      console.log(res);
      this.router.navigateByUrl('/app');
      this.dialogRef.close();
    });
  }
}
