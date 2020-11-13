import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class NavigationService {
  private isSidenavToggled = false;
  private sidenavToggledSubject = new BehaviorSubject<boolean>(
    this.isSidenavToggled
  );
  public sidenavToggled$ = this.sidenavToggledSubject.asObservable();

  constructor() {}

  public toggleSidenav() {
    this.isSidenavToggled = !this.isSidenavToggled;
    this.sidenavToggledSubject.next(this.isSidenavToggled);
  }
}
