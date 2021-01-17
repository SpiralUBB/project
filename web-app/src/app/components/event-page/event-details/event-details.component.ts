import { Component, EventEmitter, Input, OnChanges, OnInit, Output } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { circle, Circle, icon, latLng, marker, Marker } from 'leaflet';
import { of } from 'rxjs';
import { catchError, filter, map, mergeMap, take } from 'rxjs/operators';
import { AppEvent } from 'src/app/models/app-event.interface';
import { Invitation } from 'src/app/models/invitation.interface';
import { ApiService } from 'src/app/services/api.service';
import { AuthService } from 'src/app/services/auth.service';
import { MapService } from 'src/app/services/map.service';
import { EventFormComponent } from '../../event-form/event-form.component';
import { ConfirmPopupComponent } from '../../shared/confirm-popup/confirm-popup.component';

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.scss'],
})
export class EventDetailsComponent implements OnInit, OnChanges {
  @Input() eventId: string;
  @Input() showJoinButton = false;
  @Input() invitationStatus: string;
  @Input() isOwner: boolean;
  @Output() joinedEvent = new EventEmitter<Invitation>();
  event: AppEvent;
  selectedEventMarker: Marker | Circle;
  isLoggedIn: boolean;
  invitation: Invitation;

  constructor(
    private apiService: ApiService,
    public mapService: MapService,
    private authService: AuthService,
    private dialog: MatDialog,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.isLoggedIn().subscribe((isLoggedIn) => (this.isLoggedIn = isLoggedIn));
  }

  ngOnChanges(): void {
    this.loadEvent();
  }

  loadEvent(id?: string): void {
    this.apiService
      .getEventById(id ?? this.eventId)
      .pipe(
        mergeMap((event: AppEvent) =>
          this.apiService.getEventInvitationForUser(event.id).pipe(
            catchError((e) => of(null)),
            map((invitation) => ({ invitation, event }))
          )
        )
      )
      .subscribe(({ event, invitation }) => {
        this.setEventRes(event);
        this.invitation = invitation;
      });
  }

  setEventRes(res: AppEvent): void {
    const markerLatLng = latLng(res.locationPoints[0], res.locationPoints[1]);

    if (res.isLimitedDetails) {
      this.selectedEventMarker = circle(markerLatLng, {
        radius: res.locationPointsRadiusMeters,
      });
    } else {
      this.selectedEventMarker = marker(markerLatLng, {
        icon: icon({
          iconSize: [21, 37],
          iconAnchor: [10, 37],
          iconUrl: 'assets/pin.svg',
        }),
      });
    }

    this.mapService.map.zoom = 14;
    this.mapService.map.center = markerLatLng;
    this.event = res;
  }

  joinEvent(): void {
    this.apiService.joinEvent(this.eventId).subscribe((invitation) => {
      this.joinedEvent.emit(invitation);
      this.loadEvent();
    });
  }

  deleteEvent(): void {
    const dialogRef = this.dialog.open(ConfirmPopupComponent, {
    });

    dialogRef.afterClosed().pipe(
      filter(res => res),
      mergeMap(deleteConfirmResult => this.apiService.deleteEvent(this.eventId))
    ).subscribe(event => {
      this.router.navigate(['/events']);
    });
  }

  editEvent(): void {
    console.log(this.event);
    const dialogRef = this.dialog.open(EventFormComponent, {
      data: {
        event: this.event,
      },
    });

    dialogRef.afterClosed().subscribe(() => {
      this.loadEvent();
    });
  }
}
