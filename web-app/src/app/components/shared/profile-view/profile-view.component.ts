import { Component } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { User } from 'src/app/models/user';
import { AuthService } from 'src/app/services/auth.service';
import { ProfileFormComponent } from '../profile-form/profile-form.component';

@Component({
  selector: 'app-profile-view',
  templateUrl: './profile-view.component.html',
  styleUrls: ['./profile-view.component.scss'],
})
export class ProfileViewComponent {
  user: User = null;
  pointsToNextLevel: number;

  constructor(private authService: AuthService, private router: Router, private dialog: MatDialog) {
    authService.currentUser$.subscribe(user => {
      if (!user) {
        return;
      }

      this.user = user;
      this.pointsToNextLevel = this.user.points % 100;
    });
  }

  editProfile(): void {
    this.dialog.open(ProfileFormComponent, {
      disableClose: true,
      autoFocus: true,
    });
  }

  close(): void {
    this.router.navigateByUrl('/events');
  }
}
