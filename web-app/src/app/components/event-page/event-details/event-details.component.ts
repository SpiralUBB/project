import { Component, EventEmitter, Input, OnChanges, OnInit, Output } from '@angular/core';
import { circle, Circle, icon, latLng, marker, Marker } from 'leaflet';
import { take } from 'rxjs/operators';
import { AppEvent } from 'src/app/models/app-event.interface';
import { Invitation } from 'src/app/models/invitaion.interface';
import { ApiService } from 'src/app/services/api.service';
import { MapService } from 'src/app/services/map.service';

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.scss'],
})
export class EventDetailsComponent implements OnInit, OnChanges {
  @Input() eventId: string;
  @Input() showJoinButton: boolean = false;
  @Input() invitationStatus: string;
  @Output() joinedEvent = new EventEmitter<Invitation>();
  appEvent: AppEvent;
  selectedEventMarker: Marker | Circle;

  constructor(private apiService: ApiService, private mapService: MapService) {}

  ngOnInit(): void {}

  ngOnChanges(): void {
    this.loadEvent();
  }

  loadEvent(id?: string) {
    this.apiService
      .getEventById(id ?? this.eventId)
      .pipe(take(1))
      .subscribe((res: AppEvent) => {
        this.setEventRes(res);
      });
  }

  setEventRes(res: AppEvent) {
    const markerLatLng = latLng(res.locationPoints[0], res.locationPoints[1]);

    if (res.isLimitedDetails) {
      this.selectedEventMarker = circle(markerLatLng, {
        radius: res.locationPointsRadiusMeters
      })
    } else {
      this.selectedEventMarker = marker(markerLatLng, {
        icon: icon({
          iconSize: [25, 41],
          iconAnchor: [13, 41],
          iconUrl: 'leaflet/marker-icon.png',
          shadowUrl: 'leaflet/marker-shadow.png',
        }),
      });
    }

    this.mapService.map.zoom = 14;
    this.mapService.map.center = markerLatLng;
    this.appEvent = res;
    console.log(this.appEvent);
  }

  joinEvent() {
    this.apiService.joinEvent(this.eventId).subscribe((invitation) => {
      this.joinedEvent.emit(invitation);
      this.loadEvent();
    })
  }
}
