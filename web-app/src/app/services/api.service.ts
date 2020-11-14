import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoginUser } from '../models/login-user.interface';
import { RegisterUser } from '../models/register-user.interface';
import { User } from '../models/user';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  login(user: LoginUser): Observable<User>{
    return this.http.post<User>('/user/login', user);
  }

  register(user: RegisterUser): Observable<RegisterUser>{
    return this.http.post<RegisterUser>('/user/register',user);
  }
}