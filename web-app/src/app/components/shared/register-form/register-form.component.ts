import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-register-form',
  templateUrl: './register-form.component.html',
  styleUrls: ['./register-form.component.scss']
})
export class RegisterFormComponent implements OnInit {

  hasRegisterError = false;
  
  constructor(private apiService: ApiService, private router: Router) {}

  ngOnInit(): void {
  }

  register(firstName: string, lastName: string, username: string, password: string){
      this.apiService.register(firstName,lastName,username,password).subscribe((res) => {
        this.router.navigateByUrl('/login');
      });
    }
}
