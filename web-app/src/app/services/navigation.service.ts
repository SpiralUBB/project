import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { MenuEntry } from '../models/menu-entry.interface';

@Injectable({
  providedIn: 'root',
})
export class NavigationService {
  private isSidenavToggled = false;
  private sidenavToggledSubject = new BehaviorSubject<boolean>(this.isSidenavToggled);
  public sidenavToggled$ = this.sidenavToggledSubject.asObservable();

  constructor() {}
  menuEntries: MenuEntry[] = [
    { title: 'All Events', url: '/events' },
    { title: 'History events', url: '/event-history' },
    { title: 'Upcoming events', url: '/event-upcoming' },
    { title: 'Map', url: '/map' },
    { title: 'Profile', url: '/profile' },
  ];

  visitorMenuEntries: MenuEntry[] = [
    { title: 'All Events', url: '/events' },
    { title: 'Map', url: '/map' },
  ];

  public toggleSidenav(): void {
    this.isSidenavToggled = !this.isSidenavToggled;
    this.sidenavToggledSubject.next(this.isSidenavToggled);
  }
}
