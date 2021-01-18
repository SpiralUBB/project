import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { User } from 'src/app/models/user';
import { AuthService } from 'src/app/services/auth.service';
import { ProfileFormComponent } from '../profile-form/profile-form.component';
import { ApiService } from '../../../services/api.service';
import { UserFeedback } from '../../../models/user-feedback.interface';

@Component({
  selector: 'app-profile-view',
  templateUrl: './profile-view.component.html',
  styleUrls: ['./profile-view.component.scss'],
})
export class ProfileViewComponent implements OnInit {
  user: User = null;
  pointsToNextLevel: number;
  feedbacks: UserFeedback[];

  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private router: Router,
    private dialog: MatDialog
  ) {
    authService.currentUser$.subscribe((user) => {
      if (!user) {
        return;
      }

      this.user = user;
      this.pointsToNextLevel = this.user.points % 100;
    });
  }

  ngOnInit(): void {
    this.apiService.getUserFeedbacks().subscribe((feedbacks) => {
      this.feedbacks = feedbacks.items;
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
