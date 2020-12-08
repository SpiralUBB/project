import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AppEvent } from '../models/app-event.interface';
import { LoginUser } from '../models/login-user.interface';
import { RegisterUser } from '../models/register-user.interface';
import { User } from '../models/user';
import { AppComment } from '../models/comment.interface'
import { ApiResponse } from '../models/api-response.interface';
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

  logout(): Observable<any> {
    return this.http.post<any>('/user/logout', null);
  }

  addComment(text: string, eventId: string): Observable<AppComment> {
    return this.http.post<any>('/events/' + eventId + '/comments', {text: text});
  }

  deleteComment(eventId: string, commentId: string): Observable<AppComment>{
    return this.http.delete<any>('/events/' + eventId + '/comments/' + commentId);
  }

  getComments(eventId: string): Observable<ApiResponse<AppComment>> {
    return this.http.get<any>('/events/' + eventId + '/comments')
  }
}
