import { Injectable, NgZone } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Circle, icon, latLng, Marker, marker, tileLayer } from 'leaflet';
import { MarkerPopupComponent } from '../components/map/marker-popup/marker-popup.component';
import { AppEvent } from '../models/app-event.interface';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root',
})
export class MapService {
  private events: AppEvent[] = [];
  public eventsLayer: Marker[];

  public map = {
    zoom: 5,
    center: latLng(46.879966, -121.726909),
  };

  public readonly options = {
    layers: [
      tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 20,
        attribution: '...',
      }),
    ],
    zoom: 7,
    center: latLng(46.879966, -121.726909),
  };

  constructor(
    private apiService: ApiService,
    private dialog: MatDialog,
    private ngZone: NgZone
  ) {
    this.initMap();
  }

  initMap() {
    // marker([46.879966, -121.726909]);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        this.map.center = latLng(latitude, longitude);
        this.map.zoom = 15;
      });
    }

    this.apiService.getAllEvents().subscribe((eventsRes) => {
      Object.keys(eventsRes.items).forEach((key) => {
        this.events.push(eventsRes.items[key]);
      });
      console.log(this.events);
      this.eventsLayer = Object.values(this.events).map((event) =>
        marker(latLng(event.locationPoints[0], event.locationPoints[1]), {
          icon: icon({
            iconSize: [25, 41],
            iconAnchor: [13, 41],
            iconUrl: 'leaflet/marker-icon.png',
            shadowUrl: 'leaflet/marker-shadow.png',
          }),
        }).on('click', (e) => this.openEventCard(event))
      );
    });
  }

  openEventCard(event: AppEvent) {
    this.ngZone.run(() => {
      this.dialog.open(MarkerPopupComponent, {
        maxWidth: '100vw !important',
        data: { event },
      });
    });
  }
}
