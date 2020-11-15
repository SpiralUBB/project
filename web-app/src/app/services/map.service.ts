import { Injectable } from '@angular/core';
import { Circle, icon, latLng, Marker, marker, tileLayer } from 'leaflet';
import { AppEvent } from '../models/app-event.interface';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root',
})
export class MapService {
  private events: AppEvent[];
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

  constructor(private apiService: ApiService) {
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
      this.events = eventsRes;
      console.log(this.events);
      this.eventsLayer = Object.values(this.events).map((event) =>
        marker(latLng(event.locationPoints[0], event.locationPoints[1]), {
          icon: icon({
            iconSize: [25, 41],
            iconAnchor: [13, 41],
            iconUrl: 'leaflet/marker-icon.png',
            shadowUrl: 'leaflet/marker-shadow.png',
          }),
        })
      );
    });
  }
}
