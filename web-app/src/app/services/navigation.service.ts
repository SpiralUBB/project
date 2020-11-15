import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { MenuEntry } from '../models/menu-entry.interface';

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
  menuEntries: MenuEntry[] = [
    { title: 'Landing Page', url: '/landing-page' },
    { title: 'Events', url: '/app/events' },
    { title: 'Map', url: '/app/map' },
  ];

  public toggleSidenav() {
    this.isSidenavToggled = !this.isSidenavToggled;
    this.sidenavToggledSubject.next(this.isSidenavToggled);
  }
}
