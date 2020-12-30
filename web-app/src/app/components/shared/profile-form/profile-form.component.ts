import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/models/user';
import { AuthService } from 'src/app/services/auth.service';
import { Router } from '@angular/router';
import { MatDialogRef } from '@angular/material/dialog';


@Component({
  selector: 'app-profile-form',
  templateUrl: './profile-form.component.html',
  styleUrls: ['./profile-form.component.scss']
})
export class ProfileFormComponent implements OnInit {
  profile: User;
  points: Number;
  constructor(private authService:AuthService, private dialogRef: MatDialogRef<ProfileFormComponent>) {
    this.profile=authService.currentUserValue;
    this.points=this.profile.points%100;
  }

  updateProfile(username: string, firstName: string, lastName: string){
    //TODO
  }

  close() {
    this.dialogRef.close();
}


  ngOnInit(): void {
  }

}
