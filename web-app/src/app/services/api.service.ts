import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AppEvent } from '../models/app-event.interface';
import { LoginUser } from '../models/login-user.interface';
import { RegisterUser } from '../models/register-user.interface';
import { User } from '../models/user';
import { AppComment } from '../models/comment.interface';
import { ApiResponse } from '../models/api-response.interface';
import { Invitation } from '../models/invitation.interface';
import { retry } from 'rxjs/operators';
@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(private http: HttpClient) {}

  login(user: LoginUser): Observable<User> {
    return this.http.post<User>('/user/login', user).pipe(retry(3));
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

  getFilterEvents(
    categories: string[],
    startDate: string,
    endDate: string,
    own = false,
    invitationStatus = null,
    invitationAttendStatus = null
  ): Observable<any> {
    let params: HttpParams = new HttpParams();

    if (own === true) {
      params = params.append('own', 'true');
    }
    // if (own === false) {
    //   params = params.append('own', 'false');
    // }

    if (categories) {
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

    if (invitationStatus) {
      params = params.append('invitation_status', invitationStatus);
    }

    if (invitationAttendStatus) {
      params = params.append('invitation_attend_status', invitationAttendStatus);
    }

    return this.http.get<any>('/events', { params });
  }

  getCategories(): Observable<any> {
    return this.http.get<string[]>('/events/categories');
  }

  logout(): Observable<any> {
    return this.http.post<any>('/user/logout', null);
  }

  addComment(text: string, eventId: string): Observable<AppComment> {
    return this.http.post<any>('/events/' + eventId + '/comments', { text });
  }

  deleteComment(eventId: string, commentId: string): Observable<AppComment> {
    return this.http.delete<any>('/events/' + eventId + '/comments/' + commentId);
  }

  getComments(eventId: string): Observable<ApiResponse<AppComment>> {
    return this.http.get<any>('/events/' + eventId + '/comments');
  }

  getEventById(id: string): Observable<AppEvent> {
    return this.http.get<AppEvent>('/events/' + id);
  }

  getEventInvitationForUser(id: string): Observable<Invitation> {
    return this.http.get<Invitation>('/events/' + id + '/invitation');
  }

  getEventInvitations(id: string): Observable<ApiResponse<Invitation>> {
    return this.http.get<ApiResponse<Invitation>>('/events/' + id + '/invitations');
  }

  addEvent(body: any): Observable<AppEvent> {
    return this.http.post<AppEvent>('/events', body);
  }

  joinEvent(eventId: string): Observable<Invitation> {
    return this.http.put<Invitation>(`/events/${eventId}/invitation`, {});
  }

  patchInvitationStatus(
    eventId: string,
    invitationId: string,
    invitationStatus: string
  ): Observable<Invitation> {
    return this.http.patch<any>(`/events/${eventId}/invitations/${invitationId}`, {
      status: invitationStatus,
    });
  }

  patchAttendanceStatus(
    eventId: string,
    invitationId: string,
    attendStatus: string
  ): Observable<Invitation> {
    return this.http.patch<any>(`/events/${eventId}/invitations/${invitationId}`, {
      attend_status: attendStatus,
    });
  }

  putFeedback(
    username: string,
    eventId: string,
    points: number,
    message: string
  ): Observable<void> {
    const params: HttpParams = new HttpParams().set('to_user', username).set('event_id', eventId);
    return this.http.put<any>('/feedbacks', { points, message }, { params });
  }
}
