import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { latLng, tileLayer, Map } from 'leaflet';
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
  show = false;
  mapCenter;

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

  eventForm = new FormGroup({
    title: new FormControl('', [Validators.required]),
    location: new FormControl('', [Validators.required]),
    startDate: new FormControl('', [Validators.required]),
    endDate: new FormControl('', [Validators.required]),
    startTime: new FormControl('', [Validators.required]),
    endTime: new FormControl('', [Validators.required]),
    visibility: new FormControl('', [Validators.required]),
    category: new FormControl('', [Validators.required]),
    trustLevel: new FormControl('', [Validators.required]),
    x: new FormControl(0, [Validators.required]),
    y: new FormControl(0, [Validators.required]),
    nrMaxParticipants: new FormControl(0),
    textarea: new FormControl(''),
  });

  @ViewChild('textarea')
  private textarea;

  ngOnInit(): void {
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
      .subscribe((currentUser) =>
        this.addTrustLevelOptions(currentUser.trustLevel)
      );
  }

  addEventsCategories(categroiesType: any): void {
    Object.keys(categroiesType).forEach((key) => {
      const category = {
        value: key,
        viewValue: key,
      };
      this.categories.push(category);
    });
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
  }

  onChangeMaxNrParticipants(): void {
    this.show = !this.show;
  }

  onMouseOver(): void {
    if (this.textarea.nativeElement !== document.activeElement) {
      this.textarea.nativeElement.style.border = '2px solid black';
    }
  }

  onMouseLeave(): void {
    this.textarea.nativeElement.style.border = '1px solid rgb(128, 128, 128)';
  }

  addHoursMinsToDate(date: any, hoursMins: string) {
    let startTime = Date.parse(date);
    let [startHours, startMins] = hoursMins.split(':');
    let startMoment = moment(startTime)
      .add(Number(startHours), 'hours')
      .add(Number(startMins), 'minutes');
    return startMoment.toISOString();
  }

  onSubmit(): void {
    this.apiService
      .addEvent({
        title: this.eventForm.value.title,
        location: this.eventForm.value.location,
        description: this.eventForm.value.textarea,
        visibility: this.eventForm.value.visibility,
        category: this.eventForm.value.category,
        minTrustLevel: this.eventForm.value.trustLevel,
        noMaxParticipants: this.eventForm.value.nrMaxParticipants,
        locationPoint: [this.eventForm.value.x, this.eventForm.value.y],
        startTime: this.addHoursMinsToDate(this.eventForm.value.startDate, this.eventForm.value.startTime),
        endTime: this.addHoursMinsToDate(this.eventForm.value.endDate, this.eventForm.value.endTime),
        // startTime:
        //   this.eventForm.value.startDate + 'T' + this.eventForm.value.startTime,
        // endTime:
        //   this.eventForm.value.endDate + 'T' + this.eventForm.value.endTime,
      })
      .subscribe(() => {
        this.dialog.close();
      });
  }

  onMapReady(leafletMap: Map): void {
    console.log('map ready');
    leafletMap.on('click', <LeafletMouseEvent>(e) => {
      this.eventForm.patchValue({
        x: e.latlng.lat,
        y: e.latlng.lng,
      })
    });
  }
}
