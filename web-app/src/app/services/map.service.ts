import { Injectable, NgZone } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { circle, Circle, icon, latLng, Marker, marker, tileLayer } from 'leaflet';
import { MarkerPopupComponent } from '../components/map/marker-popup/marker-popup.component';
import { AppEvent } from '../models/app-event.interface';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root',
})
export class MapService {
  private events: AppEvent[] = [];
  public eventsLayer: (Marker | Circle)[];

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

  constructor(private apiService: ApiService, private dialog: MatDialog, private ngZone: NgZone) {
    this.initMap();
  }

  initMap(): void {
    // marker([46.879966, -121.726909]);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        this.map.center = latLng(latitude, longitude);
        this.map.zoom = 14;
      });
    }

    this.apiService.getAllEvents().subscribe((eventsRes) => {
      Object.keys(eventsRes.items).forEach((key) => {
        this.events.push(eventsRes.items[key]);
      });
      console.log(this.events);

      const locationEvents = new Map();
      const whiteListedEvents = new Map();
      Object.values(this.events).forEach((event: AppEvent) => {
        if (event.isLimitedDetails) {
          const location = String(event.locationPoints[0]) + ',' + String(event.locationPoints[1] + String(event.locationPointsRadiusMeters)); 
          if (!whiteListedEvents.has(location)) {
            whiteListedEvents.set(location, []);
          }

          whiteListedEvents.set(location, [...whiteListedEvents.get(location), event]);
        } else {
          const location = String(event.locationPoints[0]) + ',' + String(event.locationPoints[1]); 
          if (!locationEvents.has(location)) {
            locationEvents.set(location, []);
          }

          locationEvents.set(location, [...locationEvents.get(location), event]);
        }
      });

      this.eventsLayer = [];
      locationEvents.forEach((events, locationPoints) => {
        const m = marker(latLng(events[0].locationPoints[0], events[0].locationPoints[1]), {
          icon: icon({
            iconSize: [25, 41],
            iconAnchor: [13, 41],
            iconUrl: 'leaflet/marker-icon.png',
            shadowUrl: 'leaflet/marker-shadow.png',
          }),
        }).on('click', (e) => this.openEventCard(events));

        this.eventsLayer.push(m);
      });

      whiteListedEvents.forEach((events: AppEvent[], locationPoints) => {
        const m = circle(latLng(events[0].locationPoints[0], events[0].locationPoints[1]), {
          radius: events[0].locationPointsRadiusMeters,
        }).on('click', (e) => this.openEventCard(events));

        this.eventsLayer.push(m);
      });
    });
  }

  openEventCard(events: AppEvent[]): void {
    this.ngZone.run(() => {
      this.dialog.open(MarkerPopupComponent, {
        data: { events },
        width: '765px',
      });
    });
  }
}
