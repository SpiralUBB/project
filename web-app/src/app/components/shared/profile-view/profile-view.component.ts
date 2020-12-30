import { Component, OnInit } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { User } from 'src/app/models/user';
import { AuthService } from 'src/app/services/auth.service';
import { ProfileFormComponent } from '../profile-form/profile-form.component';

@Component({
  selector: 'app-profile-view',
  templateUrl: './profile-view.component.html',
  styleUrls: ['./profile-view.component.scss']
})
export class ProfileViewComponent implements OnInit {
  profile: User;
  points: Number;
  
  constructor(private authService:AuthService, private router: Router,private dialog: MatDialog) {
    this.profile=authService.currentUserValue;
    this.points=this.profile.points%100;
  }

  editProfile(){
    const dialogConfig = new MatDialogConfig();

    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    const dialogRef = this.dialog.open(ProfileFormComponent, dialogConfig);
  }

  close(){
    this.router.navigateByUrl('/app/events');
  }

  ngOnInit(): void {
  }

}
