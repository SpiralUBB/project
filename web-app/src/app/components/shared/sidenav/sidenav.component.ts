import { Component, OnInit } from '@angular/core';
import { NavigationService } from 'src/app/services/navigation.service';

@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrls: ['./sidenav.component.scss']
})
export class SidenavComponent implements OnInit {
  // @ViewChild('drawer') drawerElementRef: ElementRef;

  constructor(public navigationService: NavigationService) { }

  ngOnInit(): void {
    this.navigationService.sidenavToggled$.subscribe((val) => {
      // this.drawerElementRef.nativeElement.toggl
      console.log(val);
    });
  }
}
