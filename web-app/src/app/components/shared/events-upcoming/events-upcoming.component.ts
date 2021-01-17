import { Component, OnInit } from '@angular/core';
import { AppEvent } from 'src/app/models/app-event.interface';
import { ApiService } from 'src/app/services/api.service';
import { AuthService } from 'src/app/services/auth.service';
import { DatePipe, formatDate } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { EventFormComponent } from '../../event-form/event-form.component';

@Component({
  selector: 'app-events-upcoming',
  templateUrl: './events-upcoming.component.html',
  styleUrls: ['./events-upcoming.component.scss'],
})
export class EventsUpcomingComponent implements OnInit {
  eventsCreatedFuture: AppEvent[] = [];
  eventsAcceptedFuture: AppEvent[] = [];
  isLoggedIn: boolean;

  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private datePipe: DatePipe,
    private dialog: MatDialog, 
    private router: Router
  ) {}

  ngOnInit(): void {
    this.apiService
      .getFilterEvents([], this.datePipe.transform(new Date(), 'yyyy-MM-dd'), null, true)
      .subscribe((eventsRes) => {
        Object.keys(eventsRes.items).forEach((key) => {
          this.eventsCreatedFuture.push(eventsRes.items[key]);
        });
      });
    this.apiService
      .getFilterEvents(
        [],
        this.datePipe.transform(new Date(), 'yyyy-MM-dd'),
        null,
        false,
        'accepted'
      )
      .subscribe((eventsRes) => {
        Object.keys(eventsRes.items).forEach((key) => {
          this.eventsAcceptedFuture.push(eventsRes.items[key]);
        });
      });
    this.authService.isLoggedIn().subscribe(isLoggedIn => this.isLoggedIn = isLoggedIn);
  }

  openEventFormDialog(): void {
    const dialogRef = this.dialog.open(EventFormComponent);
    dialogRef.afterClosed().subscribe(() => {
      this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
        this.router.navigate(['/event-upcoming']);
      });
    });
  }
}
