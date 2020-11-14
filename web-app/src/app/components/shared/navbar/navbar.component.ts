import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { NavigationService } from 'src/app/services/navigation.service';
import { LoginFormComponent } from '../login-form/login-form.component';
import { RegisterFormComponent } from '../register-form/register-form.component';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {
  constructor(
    private dialog: MatDialog,
    private navigationService: NavigationService,
    private authService: AuthService
  ) {}
  isLoggedIn: boolean;

  ngOnInit(): void {
    this.authService.currentUser$.subscribe((currentUser) =>{
      this.isLoggedIn = !!currentUser;
    });
  
  }

  openLoginDialog() {
    const dialogRef = this.dialog.open(LoginFormComponent);
  }

  openRegisterDialog() {
    const dialogRef = this.dialog.open(RegisterFormComponent);
  }

  logout(){
      this.authService.logout();
  }

  toggleSidenav() {
    this.navigationService.toggleSidenav();
  }
}
