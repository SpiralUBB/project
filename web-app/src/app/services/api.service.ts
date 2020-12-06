import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AppEvent } from '../models/app-event.interface';
import { LoginUser } from '../models/login-user.interface';
import { RegisterUser } from '../models/register-user.interface';
import { User } from '../models/user';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(private http: HttpClient) {}

  login(user: LoginUser): Observable<User> {
    return this.http.post<User>('/user/login', user);
  }

  getCurrentUser(): Observable<User> {
    return this.http.get<User>('/user');
  }

  register(user: RegisterUser): Observable<RegisterUser> {
    return this.http.post<RegisterUser>('/user/register', user);
  }

  getAllEvents(): Observable<any> {
    return this.http.get<AppEvent[]>('/events');
  }

  getFilterEvents(categories:String[],startDate:String,endDate:String): Observable<any>{
    var url="/events?";
    for(let i=0;i<categories.length;i++){
      url+="category="+categories[i].replace("&","%26")+"&";
    }
    if(startDate!=null)
      url+="start_date="+startDate+"&";
    if(endDate!=null)
      url+="end_date="+endDate+"&";
    url=url.slice(0,-1);
    console.log(url);
    return this.http.get<any>(url);
  }

  getCategories(): Observable<any>{
    return this.http.get<String[]>('/events/categories');
  }

  logout(): Observable<any> {
    return this.http.post<any>('/user/logout', null);
  }
}
