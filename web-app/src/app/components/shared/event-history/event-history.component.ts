import { Component, OnInit } from '@angular/core';
import { AppEvent } from 'src/app/models/app-event.interface';
import { ApiService } from 'src/app/services/api.service';
import { AuthService } from 'src/app/services/auth.service';
import { DatePipe, formatDate } from '@angular/common';

@Component({
  selector: 'app-event-history',
  templateUrl: './event-history.component.html',
  styleUrls: ['./event-history.component.scss'],
})
export class EventHistoryComponent implements OnInit {
  eventsCreatedPast: AppEvent[] = [];
  eventsParticipated: AppEvent[] = [];

  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private datePipe: DatePipe
  ) {}

  ngOnInit(): void {
    this.apiService
      .getFilterEvents(
        [],
        null,
        this.datePipe.transform(new Date(), 'yyyy-MM-dd'),
        true,
      )
      .subscribe((eventsRes) => {
        Object.keys(eventsRes.items).forEach((key) => {
          this.eventsCreatedPast.push(eventsRes.items[key]);
        });
      });
    this.apiService.getFilterEvents(
        [],
        null,
        this.datePipe.transform(new Date(), 'yyyy-MM-dd'),
        null,
        false,
        'attended'
      )
      .subscribe((eventsRes) => {
      Object.keys(eventsRes.items).forEach((key) => {
        this.eventsParticipated.push(eventsRes.items[key]);
      });
    });
  }
}
