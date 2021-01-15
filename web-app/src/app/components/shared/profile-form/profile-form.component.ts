import { Component } from '@angular/core';
import { User } from 'src/app/models/user';
import { AuthService } from 'src/app/services/auth.service';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-profile-form',
  templateUrl: './profile-form.component.html',
  styleUrls: ['./profile-form.component.scss'],
})
export class ProfileFormComponent {
  profile: User;
  points: number;
  constructor(
    private authService: AuthService,
    private dialogRef: MatDialogRef<ProfileFormComponent>
  ) {
    this.profile = authService.currentUserValue;
    this.points = this.profile.points % 100;
  }

  updateProfile(username: string, firstName: string, lastName: string): void {
    // TODO
  }

  close(): void {
    this.dialogRef.close();
  }
}
