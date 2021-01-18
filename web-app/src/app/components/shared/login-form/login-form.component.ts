import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { MatInput } from '@angular/material/input';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.scss'],
})
export class LoginFormComponent implements OnInit {
  formStatus: any = {
    emailValue: '',
    passwordValue: '',
  };
  hasLoginError = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private dialogRef: MatDialogRef<LoginFormComponent>,
    private snackService: MatSnackBar
  ) {}

  ngOnInit(): void {}

  login(username: string, password: string): void {
    this.authService.login(username, password).subscribe((res) => {
      this.router.navigateByUrl('/events');
      this.dialogRef.close();
    }, (err) => {
        console.log(err);
        this.snackService.open('Failed to login. Wrong username/password');
    });
  }

  submitOnEnterKey(event): void {
    if (event.keyCode === 13) {
      this.login(this.formStatus.emailValue, this.formStatus.passwordValue);
    }
  }
}
