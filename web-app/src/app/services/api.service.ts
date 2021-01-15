import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AppEvent } from '../models/app-event.interface';
import { LoginUser } from '../models/login-user.interface';
import { RegisterUser } from '../models/register-user.interface';
import { User } from '../models/user';
import { AppComment } from '../models/comment.interface';
import { ApiResponse } from '../models/api-response.interface';
import { Invitation } from '../models/invitaion.interface';
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

  getFilterEvents(categories: string[], startDate: string, endDate: string): Observable<any> {
    let params: HttpParams = new HttpParams().set('own', 'true');

    if (categories.length > 0) {
      for (const category of categories) {
        params = params.append('category', category);
      }
    }

    if (startDate) {
      params = params.append('date_start', startDate.toString());
    }

    if (endDate) {
      params = params.append('date_end', endDate.toString());
    }

    return this.http.get<any>('/events', {params});
  }

  getCategories(): Observable<any>{
    return this.http.get<string[]>('/events/categories');
  }

  logout(): Observable<any> {
    return this.http.post<any>('/user/logout', null);
  }

  addComment(text: string, eventId: string): Observable<AppComment> {
    return this.http.post<any>('/events/' + eventId + '/comments', {text});
  }

  deleteComment(eventId: string, commentId: string): Observable<AppComment>{
    return this.http.delete<any>('/events/' + eventId + '/comments/' + commentId);
  }

  getComments(eventId: string): Observable<ApiResponse<AppComment>> {
    return this.http.get<any>('/events/' + eventId + '/comments');
  }

  getAttendedEvents(): Observable<any>{
    const params: HttpParams = new HttpParams().set('invitation_attend_status', 'attended');

    return this.http.get<any>('/events', {params});
  }

  getEventById(id: string): Observable<AppEvent> {
    return this.http.get<AppEvent>('/events/' + id);
  }


  getEventInvitaionForUser(id: string): Observable<Invitation> {
    return this.http.get<Invitation>('/events/' + id + '/invitation');
  }

  addEvent(body: any): Observable<AppEvent> {
    return this.http.post<AppEvent>('/events', body);
  }

}
