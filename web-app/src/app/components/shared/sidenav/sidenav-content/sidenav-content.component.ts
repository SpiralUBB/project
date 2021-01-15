import { Component, OnInit } from '@angular/core';
import { NavigationService } from 'src/app/services/navigation.service';

@Component({
  selector: 'app-sidenav-content',
  templateUrl: './sidenav-content.component.html',
  styleUrls: ['./sidenav-content.component.scss'],
})
export class SidenavContentComponent implements OnInit {

  constructor(public navigationService: NavigationService) { }

  ngOnInit(): void {
  }

  toggleSideNav(): void {
    this.navigationService.toggleSidenav();
  }
}
