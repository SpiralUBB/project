import { Component, EventEmitter, Input, OnChanges, OnInit, Output } from '@angular/core';
import { circle, Circle, icon, latLng, marker, Marker } from 'leaflet';
import { take } from 'rxjs/operators';
import { AppEvent } from 'src/app/models/app-event.interface';
import { Invitation } from 'src/app/models/invitation.interface';
import { ApiService } from 'src/app/services/api.service';
import { AuthService } from 'src/app/services/auth.service';
import { MapService } from 'src/app/services/map.service';

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.scss'],
})
export class EventDetailsComponent implements OnInit, OnChanges {
  @Input() eventId: string;
  @Input() showJoinButton = false;
  @Input() invitationStatus: string;
  @Output() joinedEvent = new EventEmitter<Invitation>();
  appEvent: AppEvent;
  selectedEventMarker: Marker | Circle;
  isLoggedIn: boolean;

  constructor(private apiService: ApiService, public mapService: MapService, private authService: AuthService) {}

  ngOnInit(): void {
    this.authService.isLoggedIn().subscribe(isLoggedIn => this.isLoggedIn = isLoggedIn);
  }

  ngOnChanges(): void {
    this.loadEvent();
  }

  loadEvent(id?: string): void {
    this.apiService
      .getEventById(id ?? this.eventId)
      .pipe(take(1))
      .subscribe((res: AppEvent) => {
        this.setEventRes(res);
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
    this.appEvent = res;
  }

  joinEvent(): void {
    this.apiService.joinEvent(this.eventId).subscribe((invitation) => {
      this.joinedEvent.emit(invitation);
      this.loadEvent();
    });
  }
}
