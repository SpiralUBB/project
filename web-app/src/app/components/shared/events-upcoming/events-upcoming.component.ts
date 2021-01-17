import { Component, OnInit } from '@angular/core';
import { AppEvent } from 'src/app/models/app-event.interface';
import { ApiService } from 'src/app/services/api.service';
import { AuthService } from 'src/app/services/auth.service';
import { DatePipe, formatDate } from '@angular/common';


@Component({
  selector: 'app-events-upcoming',
  templateUrl: './events-upcoming.component.html',
  styleUrls: ['./events-upcoming.component.scss'],
})
export class EventsUpcomingComponent implements OnInit {
  eventsCreatedFuture: AppEvent[] = [];
  eventsAcceptedFuture: AppEvent[] = [];

  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private datePipe: DatePipe
  ) {}

  ngOnInit(): void {
    this.apiService
      .getFilterEvents(
        [],
        this.datePipe.transform(new Date(), 'yyyy-MM-dd'),
        null,
        true
      )
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
  }
}
