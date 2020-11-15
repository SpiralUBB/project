import { Component, OnInit } from '@angular/core';
import { LatLng, latLng, tileLayer } from 'leaflet';
import { MapService } from 'src/app/services/map.service';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss'],
})
export class MapComponent implements OnInit {
  constructor(public mapService: MapService) {}

  ngOnInit(): void {}
}
