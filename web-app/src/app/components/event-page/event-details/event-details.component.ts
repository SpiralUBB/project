import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { icon, latLng, marker, Marker } from 'leaflet';
import { take } from 'rxjs/operators';
import { AppEvent } from 'src/app/models/app-event.interface';
import { ApiService } from 'src/app/services/api.service';
import { MapService } from 'src/app/services/map.service';

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.scss'],
})
export class EventDetailsComponent implements OnInit, OnChanges {
  @Input() eventId: string;
  appEvent: AppEvent;
  selectedEventMarker: Marker;

  constructor(private apiService: ApiService, private mapService: MapService) {}

  ngOnInit(): void {}

  ngOnChanges(): void {
    this.apiService
      .getEventById(this.eventId)
      .pipe(take(1))
      .subscribe((res) => {
        const markerLatLng = latLng(res.locationPoints[0], res.locationPoints[1]);
        this.selectedEventMarker = marker(markerLatLng, {
          icon: icon({
            iconSize: [25, 41],
            iconAnchor: [13, 41],
            iconUrl: 'leaflet/marker-icon.png',
            shadowUrl: 'leaflet/marker-shadow.png',
          }),
        });
        this.mapService.map.center = markerLatLng;
        this.appEvent = res;
      });
  }
}
