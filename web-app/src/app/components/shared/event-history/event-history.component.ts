import { Component, OnInit } from '@angular/core';
import { AppEvent } from 'src/app/models/app-event.interface';
import { ApiService } from 'src/app/services/api.service';
import { AuthService } from 'src/app/services/auth.service';
import { DatePipe, formatDate } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { EventFormComponent } from '../../event-form/event-form.component';

@Component({
  selector: 'app-event-history',
  templateUrl: './event-history.component.html',
  styleUrls: ['./event-history.component.scss'],
})
export class EventHistoryComponent implements OnInit {
  eventsCreatedPast: AppEvent[] = [];
  eventsParticipated: AppEvent[] = [];
  isLoggedIn: boolean;

  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private datePipe: DatePipe,
    
    private dialog: MatDialog, 
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.apiService
      .getFilterEvents([], null, this.datePipe.transform(new Date(), 'yyyy-MM-dd'), true)
      .subscribe((eventsRes) => {
        Object.keys(eventsRes.items).forEach((key) => {
          this.eventsCreatedPast.push(eventsRes.items[key]);
        });
      });
    this.apiService
      .getFilterEvents(
        [],
        null,
        this.datePipe.transform(new Date(), 'yyyy-MM-dd'),
        false,
        null,
        'attended'
      )
      .subscribe((eventsRes) => {
        Object.keys(eventsRes.items).forEach((key) => {
          this.eventsParticipated.push(eventsRes.items[key]);
        });
      });

    this.authService.isLoggedIn().subscribe(isLoggedIn => this.isLoggedIn = isLoggedIn);
  }
  
  openEventFormDialog(): void {
    const dialogRef = this.dialog.open(EventFormComponent);
    dialogRef.afterClosed().subscribe(() => {
      this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
        this.router.navigate(['/event-history']);
      });
    });
  }
}
