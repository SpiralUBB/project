import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { latLng, tileLayer, Map, Marker, marker, icon } from 'leaflet';
import { Observable } from 'rxjs';
import { filter, map, take } from 'rxjs/operators';
import { ApiService } from 'src/app/services/api.service';
import * as moment from 'moment';

interface CheckBoxSelection {
  value: number | string;
  viewValue: number | string;
}

@Component({
  selector: 'app-event-form',
  templateUrl: './event-form.component.html',
  styleUrls: ['./event-form.component.scss'],
})
export class EventFormComponent implements OnInit {
  constructor(
    private activatedRoute: ActivatedRoute,
    private apiService: ApiService,
    private dialog: MatDialogRef<EventFormComponent>
  ) {}
  eventId$: Observable<string>;
  categories: CheckBoxSelection[] = [];
  trustLevelOptions: CheckBoxSelection[] = [];
  showParticipantsLimit = false;
  mapCenter;
  newLocationMarker: Marker;
  eventForm: FormGroup;

  public readonly locationPickerOptions = {
    layers: [
      tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 20,
        attribution: '...',
      }),
    ],
    zoom: 7,
    center: latLng(46.879966, -121.726909),
  };

  addLeadingZeros(n: number): string {
    return (n < 10 ? '0' : '') + n;
  }

  getTimeFormat(date: Date): string {
    return [date.getHours(), date.getMinutes()]
      .map(this.addLeadingZeros, this)
      .join(':');
  }

  getDateNextHour(date: Date = new Date()): Date {
    const newDate = new Date(date);
    newDate.setHours(date.getHours() + 1);
    newDate.setMinutes(0);
    return newDate;
  }

  ngOnInit(): void {
    const initialStartDate = this.getDateNextHour();
    const initialEndDate = this.getDateNextHour(initialStartDate);
    const initialStartTime = this.getTimeFormat(initialStartDate);
    const initialEndTime = this.getTimeFormat(initialEndDate);

    this.eventForm = new FormGroup({
      title: new FormControl('', [Validators.required]),
      location: new FormControl('', [Validators.required]),
      startDate: new FormControl(initialStartDate, [Validators.required]),
      endDate: new FormControl(initialEndDate, [Validators.required]),
      startTime: new FormControl(initialStartTime, [Validators.required]),
      endTime: new FormControl(initialEndTime, [Validators.required]),
      visibility: new FormControl('public', [Validators.required]),
      category: new FormControl('', [Validators.required]),
      trustLevel: new FormControl('', [Validators.required]),
      x: new FormControl(0, [Validators.required]),
      y: new FormControl(0, [Validators.required]),
      nrMaxParticipants: new FormControl(0),
      description: new FormControl('', [Validators.required]),
    });

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        this.mapCenter = latLng(latitude, longitude);
      });
    }

    this.eventId$ = this.activatedRoute.params.pipe(
      filter((params) => !!params.id),
      map((params) => params.id)
    );

    this.apiService
      .getCategories()
      .pipe(take(1))
      .subscribe((res) => this.addEventsCategories(res));

    this.apiService
      .getCurrentUser()
      .pipe(take(1))
      .subscribe((currentUser) => this.addTrustLevelOptions(currentUser.trustLevel));
  }

  addEventsCategories(categoriesType: any): void {
    let initialValue = null;

    Object.keys(categoriesType).forEach((key) => {
      const category = {
        value: key,
        viewValue: categoriesType[key],
      };

      if (!initialValue) {
        initialValue = key;
      }
      this.categories.push(category);
    });

    if (initialValue) {
      this.eventForm.patchValue({
        category: initialValue,
      });
    }
  }

  addTrustLevelOptions(currentUserTrustLevel: number): void {
    const noMinRequired = {
      value: 0,
      viewValue: 'Any trust level',
    };
    this.trustLevelOptions.push(noMinRequired);

    for (let i = 1; i < currentUserTrustLevel; i++) {
      const checkBoxOption = {
        value: i,
        viewValue: i,
      };
      this.trustLevelOptions.push(checkBoxOption);
    }

    this.eventForm.patchValue({
      trustLevel: 0,
    });
  }

  onChangeMaxNrParticipants(): void {
    this.showParticipantsLimit = !this.showParticipantsLimit;
  }

  addHoursMinsToDate(date: any, hoursMins: string): string {
    const startTime = Date.parse(date);
    const [startHours, startMins] = hoursMins.split(':');
    const startMoment = moment(startTime)
      .add(Number(startHours), 'hours')
      .add(Number(startMins), 'minutes');
    return startMoment.toISOString();
  }

  onSubmit(): void {
    this.apiService
      .addEvent({
        title: this.eventForm.value.title,
        location: this.eventForm.value.location,
        description: this.eventForm.value.description,
        visibility: this.eventForm.value.visibility,
        category: this.eventForm.value.category,
        minTrustLevel: this.eventForm.value.trustLevel,
        noMaxParticipants: this.eventForm.value.nrMaxParticipants,
        locationPoint: [this.eventForm.value.x, this.eventForm.value.y],
        startTime: this.addHoursMinsToDate(
          this.eventForm.value.startDate,
          this.eventForm.value.startTime
        ),
        endTime: this.addHoursMinsToDate(
          this.eventForm.value.endDate,
          this.eventForm.value.endTime
        ),
      })
      .subscribe(() => {
        this.dialog.close();
      });
  }

  onMapReady(leafletMap: Map): void {
    leafletMap.on('click', <LeafletMouseEvent>(e) => {
      this.eventForm.patchValue({
        x: e.latlng.lat,
        y: e.latlng.lng,
      });

      if (this.newLocationMarker) {
        this.newLocationMarker.remove();
      }

      this.newLocationMarker = marker(latLng(e.latlng.lat, e.latlng.lng), {
        icon: icon({
          iconSize: [21, 37],
          iconAnchor: [10, 37],
          iconUrl: 'assets/pin.svg',
        }),
      });

      // leafletMap
      this.newLocationMarker.addTo(leafletMap);

      // leafletMap.addLayer(
      //   [this.newLocationMarker
      // );
    });
  }
}
