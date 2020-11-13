import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoginUser } from '../models/login-user.interface';
import { User } from '../models/user';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  login(user: LoginUser): Observable<User>{
    return this.http.post<User>('/user/login', user);
  }

  register(firstName: string, lastName: string, username: string, password: string){
    var userRegister={first_name: firstName, last_name: lastName, username: username, password: password};
    return this.http.post<any>('/user/register',userRegister);
  }
}
