import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { User } from '../models/user';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private currentUserSubject: BehaviorSubject<User>;
  public currentUser$: Observable<User>;
  private triedToLogin = false;

  constructor(private apiService: ApiService, private router: Router) {
    this.currentUserSubject = new BehaviorSubject<User>(null);
    this.currentUser$ = this.currentUserSubject.asObservable();

    this.apiService.getCurrentUser().subscribe((user) => {
      this.currentUserSubject.next(user);
    });
  }

  public isAuthenticated(): Observable<boolean> {
    if (this.triedToLogin) {
      return of(!!this.currentUserSubject.value);
    } else {
      return this.apiService.getCurrentUser().pipe(
        tap((currentUser) => {
          this.triedToLogin = true;
          this.currentUserSubject.next(currentUser);
        }),
        map((currentUser) => !!currentUser)
      );
    }
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
      this.router.navigateByUrl('/landing-page');
    });
  }
}
