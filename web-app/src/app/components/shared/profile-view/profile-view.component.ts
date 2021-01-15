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
  profile: User;
  points: number;

  constructor(private authService: AuthService, private router: Router, private dialog: MatDialog) {
    this.profile = authService.currentUserValue;
    this.points = this.profile.points % 100;
  }

  editProfile(): void {
    const dialogConfig = new MatDialogConfig();

    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    this.dialog.open(ProfileFormComponent, dialogConfig);
  }

  close(): void {
    this.router.navigateByUrl('/app/events');
  }
}
