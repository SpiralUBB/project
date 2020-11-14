import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { User } from '../models/user';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private currentUserSubject: BehaviorSubject<User>;
  public currentUser$: Observable<User>;

  constructor(
    private apiService: ApiService, 
    private router: Router
  ) {
    this.currentUserSubject = new BehaviorSubject<User>(null);
    this.currentUser$ = this.currentUserSubject.asObservable();
  }

  public isAuthenticated() {
    return !!this.currentUserSubject.value;
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

  logout() {  
    this.apiService.logout().subscribe(() => {
      this.currentUserSubject.next(null);
      this.router.navigateByUrl("/landing-page");
    })
  }
}
