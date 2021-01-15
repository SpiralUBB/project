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
    private authService: AuthService,
    private router: Router
  ) {}
  isLoggedIn: boolean;

  ngOnInit(): void {
    this.authService.currentUser$.subscribe((currentUser) => {
      this.isLoggedIn = !!currentUser;
    });

  }

  openLoginDialog(): void {
    this.dialog.open(LoginFormComponent);
  }

  openRegisterDialog(): void {
    this.dialog.open(RegisterFormComponent);
  }

  openProfile(): void {
    this.router.navigateByUrl('/app/profile');
  }

  logout(): void {
      this.authService.logout();
  }

  toggleSidenav(): void {
    this.navigationService.toggleSidenav();
  }
}
