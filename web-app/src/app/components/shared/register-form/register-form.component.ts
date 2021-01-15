import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-register-form',
  templateUrl: './register-form.component.html',
  styleUrls: ['./register-form.component.scss']
})
export class RegisterFormComponent implements OnInit {

  constructor(private apiService: ApiService, private router: Router,
              private dialogRef: MatDialogRef<RegisterFormComponent>, private snackbar: MatSnackBar) {}

  ngOnInit(): void {
  }

  register(firstName: string, lastName: string, username: string, password: string): void {
      this.apiService.register({username, password, firstName, lastName}).subscribe((res) => {
        this.snackbar.open('User registered!');
        this.dialogRef.close();
      });
    }
}
