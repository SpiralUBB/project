import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/models/user';
import { AuthService } from 'src/app/services/auth.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-profile-form',
  templateUrl: './profile-form.component.html',
  styleUrls: ['./profile-form.component.scss']
})
export class ProfileFormComponent implements OnInit {
  profile: User;
  constructor(private authService:AuthService, private router: Router) {
    this.profile=authService.currentUserValue;
  }

  updateProfile(username: string, firstName: string, lastName: string){
    //TODO
  }

  close(){
    this.router.navigateByUrl('/app/events');
  }
  ngOnInit(): void {
  }

}
