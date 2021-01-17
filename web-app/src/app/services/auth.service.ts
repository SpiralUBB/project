import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { filter, map, tap } from 'rxjs/operators';
import { User } from '../models/user';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private currentUserSubject = new BehaviorSubject<User>(undefined);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private apiService: ApiService, private router: Router) {
    this.getUserData();
  }

  public getUserData(): void {
    this.apiService.getCurrentUser().subscribe(
      (user) => {
        this.currentUserSubject.next(user);
      },
      (err) => {
        this.currentUserSubject.next(null);
      }
    );
  }

  public isLoggedIn(): Observable<boolean> {
    return this.currentUser$.pipe(
      filter((user) => user !== undefined),
      map((user) => !!user)
    );
    // if (this.triedToLogin) {
    //   return of(!!this.currentUserSubject.value);
    // } else {
    //   return this.apiService.getCurrentUser().pipe(
    //     tap((currentUser) => {
    //       this.triedToLogin = true;
    //       this.currentUserSubject.next(currentUser);
    //     }),
    //     map((currentUser) => !!currentUser)
    //   );
    // }
  }

  public get currentUserValue(): User {
    return this.currentUserSubject.value;
  }

  login(username: string, password: string): Observable<any> {
    return this.apiService.login({ username, password }).pipe(
      tap((res) => {
        this.currentUserSubject.next(res);
      })
    );
  }

  logout(): void {
    this.apiService.logout().subscribe(() => {
      this.currentUserSubject.next(null);
      this.router.navigateByUrl('/events');
    });
  }
}
