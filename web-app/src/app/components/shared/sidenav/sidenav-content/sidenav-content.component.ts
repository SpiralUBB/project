import { Component, OnInit } from '@angular/core';
import { MenuEntry } from 'src/app/models/menu-entry.interface';
import { AuthService } from 'src/app/services/auth.service';
import { NavigationService } from 'src/app/services/navigation.service';

@Component({
  selector: 'app-sidenav-content',
  templateUrl: './sidenav-content.component.html',
  styleUrls: ['./sidenav-content.component.scss'],
})
export class SidenavContentComponent implements OnInit {
  constructor(
    public navigationService: NavigationService,
    private authService: AuthService
  ) { }

  isLoggedIn: boolean;
  menuEntries: MenuEntry[];

  ngOnInit(): void {
    this.authService.isLoggedIn().subscribe(isLoggedIn => {
      this.isLoggedIn = isLoggedIn;
      if (this.isLoggedIn) {
        this.menuEntries = this.navigationService.menuEntries;
      } else {
        this.menuEntries = this.navigationService.visitorMenuEntries;
      }
    });
  }

  toggleSideNav(): void {
    this.navigationService.toggleSidenav();
  }
}
