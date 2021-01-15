import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable, of } from 'rxjs';
import { catchError, filter, map, switchMap, tap } from 'rxjs/operators';
import { AppEvent } from 'src/app/models/app-event.interface';
import { Invitation } from 'src/app/models/invitaion.interface';
import { User } from 'src/app/models/user';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-event-page',
  templateUrl: './event-page.component.html',
  styleUrls: ['./event-page.component.scss'],
})
export class EventPageComponent implements OnInit {
  constructor(private activatedRoute: ActivatedRoute,
              private apiService: ApiService) {}

  public eventId$: Observable<string>;
  private id: string;
  private event: AppEvent;
  private user: User;

  private isOwner = false;
  private isEventPast = false;
  private isEventOngoing = false;
  private isEventInFuture = false;
  private isViewer = true;
  private userInvitaionType: string;

  private shouldConfirmInvitations = false;

  ngOnInit(): void {
    // daca navighezi pe un url nou unde difera doar id-ul nu se incarca pagina noua, doar se emite o alta valoare in observable
    this.eventId$ = this.activatedRoute.params.pipe(
      filter((params) => !!params.id),
      map((params) => params.id)
    );

    // Ii dai subscribe aici daca ai nevoie de el in ts
    this.eventId$.subscribe((id) => {
      this.id = id;
    });
    this.eventId$.pipe(
      switchMap((id) => {
        this.id = id;
        return this.apiService.getEventById(this.id);
      }),
      switchMap((event: AppEvent) => {
        this.event = event;
        this.compareTime(event.startTime, event.endTime);
        return this.apiService.getCurrentUser();

      }),
      switchMap((user: User) => {
        this.user = user;
        this.isOwner = this.user.username === this.event.owner.username;
        this.shouldConfirmInvitations = this.isOwner && this.isEventInFuture;
        return this.apiService.getEventInvitationForUser(this.id);
      }),
      switchMap((value: Invitation) => {
        this.userInvitaionType = value.statusText;
        this.isViewer = false;
        return of([]);
      }),
      catchError((error: any) => {
        this.isViewer = true;
        return of([]);
      })
    ).subscribe();
  }

  compareTime(startDate: string, endDate: string): void {
    const localTime = new Date().getTime();
    const startTime = new Date(startDate).getTime();
    const endTime = new Date(endDate).getTime();

    if (localTime < startTime) {
      this.isEventInFuture = true;
      this.isEventOngoing = false;
      this.isEventPast = false;
    }else{
      if (localTime < endTime) {
        this.isEventInFuture = false;
        this.isEventOngoing = true;
        this.isEventPast = false;
      }else{
        this.isEventInFuture = false;
        this.isEventOngoing = false;
        this.isEventPast = true;
      }
    }
  }
}
