import { Component, Inject, LOCALE_ID, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { GeoJSON, icon, latLng, Map, marker, Marker, tileLayer } from "leaflet";
import { Observable, Subject, Subscription } from 'rxjs';
import { filter, map, take } from 'rxjs/operators';
import { ApiService } from 'src/app/services/api.service';
import * as moment from 'moment';
import { PlaceSuggestion } from 'src/app/models/place-suggestion.interface';
import { MatOptionSelectionChange } from '@angular/material/core';
import { GeocodingService } from 'src/app/services/geocoding.service';
import { GeocodingFeatureProperties } from 'src/app/models/geocoding-feature-properties.interface';
import { ListService } from 'src/app/services/list.service';
import { AppEvent } from 'src/app/models/app-event.interface';

interface SelectOption {
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
    private dialog: MatDialogRef<EventFormComponent>,
    private geocodingService: GeocodingService,
    private listService: ListService,
    @Inject(MAT_DIALOG_DATA) public data: { event: AppEvent },
    @Inject(LOCALE_ID) public locale: string
  ) {
    this.valueChangesSub = this.inputFieldFormControl.valueChanges.subscribe((value) => {
      if (this.userInputTimeout) {
        window.clearTimeout(this.userInputTimeout);
      }

      if (this.chosenOption && this.chosenOption.shortAddress === value) {
        this.searchOptions.next(null);
        return;
      }

      if (!value || value.length < 3) {
        // do not need suggestions until for less than 3 letters
        this.searchOptions.next(null);
        return;
      }

      this.userInputTimeout = window.setTimeout(() => {
        this.generateSuggestions(value);
      }, 300);
    });
  }

  searchOptions: Subject<PlaceSuggestion[]> = new Subject<PlaceSuggestion[]>();
  inputFieldFormControl: FormControl = new FormControl();
  private valueChangesSub: Subscription;
  private userInputTimeout: number;
  private location: string;
  private chosenOption: PlaceSuggestion;
  private requestSub: Subscription;

  map: Map;
  eventId$: Observable<string>;
  categories: SelectOption[] = [];
  visibilities: SelectOption[] = [];
  trustLevelOptions: SelectOption[] = [];
  showParticipantsLimit = false;
  mapCenter;
  newLocationMarker: Marker;
  eventForm: FormGroup;

  public readonly locationPickerOptions = {
    layers: [
      tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 20,
      }),
    ],
    zoom: 7,
    center: latLng(46.879966, -121.726909),
  };

  @ViewChild('textarea')
  private textarea;

  private generateSuggestions(text: string): void {
    if (this.requestSub) {
      this.requestSub.unsubscribe();
    }

    this.requestSub = this.geocodingService.getApiCall(text).subscribe(
      (data: GeoJSON.FeatureCollection) => {
        const placeSuggestions = data.features.map((feature) => {
          const properties: GeocodingFeatureProperties = feature.properties as GeocodingFeatureProperties;

          return {
            shortAddress: this.geocodingService.generateShortAddress(properties),
            fullAddress: this.geocodingService.generateFullAddress(properties),
            data: properties,
          };
        });

        this.searchOptions.next(placeSuggestions.length ? placeSuggestions : null);
      },
      (err) => {
        console.log(err);
      }
    );
  }

  addLeadingZeros(n: number): string {
    return (n < 10 ? '0' : '') + n;
  }

  getTimeFormat(date: Date): string {
    return [date.getHours(), date.getMinutes()].map(this.addLeadingZeros, this).join(':');
  }

  getDateNextHour(date: Date = new Date()): Date {
    const newDate = new Date(date);
    newDate.setHours(date.getHours() + 1);
    newDate.setMinutes(0);
    newDate.setSeconds(0);
    return newDate;
  }

  utcStringToLocalDateTime(dateStr: string): Date {
    return moment.utc(dateStr).toDate();
  }

  addHoursMinsToDate(initialDate: Date, hoursMins: string): Date {
    const date = new Date(initialDate);
    const [hours, mins] = hoursMins
      .split(':')
      .map((p) => Number.parseInt(p, 10));
    date.setHours(hours);
    date.setMinutes(mins);
    return date;
  }

  ngOnInit(): void {
    let initialTitle: string;
    let initialStartDate: Date;
    let initialEndDate: Date;
    let initialStartTime: string;
    let initialEndTime: string;
    let initialLocationPointsX: number;
    let initialLocationPointsY: number;
    let initialNoMaxParticipants: number;
    let initialDescription: string;

    if (this.data?.event) {
      initialTitle = this.data.event.title;
      initialStartDate = this.utcStringToLocalDateTime(this.data.event.startTime);
      initialEndDate = this.utcStringToLocalDateTime(this.data.event.endTime);
      initialLocationPointsX = this.data.event.locationPoints[0];
      initialLocationPointsY = this.data.event.locationPoints[1];
      initialNoMaxParticipants = this.data.event.noMaxParticipants;
      initialDescription = this.data.event.description;

      this.inputFieldFormControl.patchValue(this.data.event.location);
      if (this.data.event.noMaxParticipants > 0) {
        this.showParticipantsLimit = true;
      }
    } else {
      initialTitle = '';
      initialStartDate = this.getDateNextHour();
      initialEndDate = this.getDateNextHour(initialStartDate);
      initialLocationPointsX = 0;
      initialLocationPointsY = 0;
      initialNoMaxParticipants = 0;
      initialDescription = '';
    }

    initialStartTime = this.getTimeFormat(initialStartDate);
    initialEndTime = this.getTimeFormat(initialEndDate);

    this.eventForm = new FormGroup({
      title: new FormControl(initialTitle, [Validators.required]),
      startDate: new FormControl(initialStartDate, [Validators.required]),
      endDate: new FormControl(initialEndDate, [Validators.required]),
      startTime: new FormControl(initialStartTime, [Validators.required]),
      endTime: new FormControl(initialEndTime, [Validators.required]),
      visibility: new FormControl('', [Validators.required]),
      category: new FormControl('', [Validators.required]),
      trustLevel: new FormControl('', [Validators.required]),
      x: new FormControl(initialLocationPointsX, [Validators.required]),
      y: new FormControl(initialLocationPointsY, [Validators.required]),
      nrMaxParticipants: new FormControl(initialNoMaxParticipants),
      description: new FormControl(initialDescription, [Validators.required]),
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
      .getVisibilities()
      .pipe(take(1))
      .subscribe((res) => this.addEventsVisibilities(res));

    this.apiService
      .getCurrentUser()
      .pipe(take(1))
      .subscribe((currentUser) => this.addTrustLevelOptions(currentUser.trustLevel));
  }

  optionsMapToList(optionsMap: any): SelectOption[] {
    const optionsList = [];

    Object.entries(optionsMap).forEach((key) => {
      optionsList.push({
        value: Number(key[0]),
        viewValue: key[1],
      });
    });

    return optionsList;
  }

  addEventsCategories(categories: any): void {
    this.categories = this.optionsMapToList(categories);

    let initialCategory = null;

    if (this.data?.event) {
      initialCategory = this.data.event.category;
    } else if (this.categories) {
      initialCategory = this.categories[0].value;
    }

    if (initialCategory != null) {
      this.eventForm.patchValue({
        category: initialCategory,
      });
    }
  }

  addEventsVisibilities(visibilities: any): void {
    this.visibilities = this.optionsMapToList(visibilities);

    let initialVisibility = null;

    if (this.data?.event) {
      initialVisibility = this.data.event.visibility;
    } else if (this.visibilities) {
      initialVisibility = this.visibilities[0].value;
    }

    if (initialVisibility != null) {
      this.eventForm.patchValue({
        visibility: initialVisibility,
      });
    }
  }

  addTrustLevelOptions(currentUserTrustLevel: number): void {
    this.trustLevelOptions.push({
      value: 0,
      viewValue: 'Any trust level',
    });

    for (let i = 1; i < currentUserTrustLevel; i++) {
      this.trustLevelOptions.push({
        value: i,
        viewValue: i,
      });
    }

    let initialMinTrustLevel;

    if (this.data?.event) {
      initialMinTrustLevel = this.data.event.minTrustLevel;
    } else {
      initialMinTrustLevel = 0;
    }

    if (initialMinTrustLevel != null) {
      this.eventForm.patchValue({
        trustLevel: initialMinTrustLevel,
      });
    }
  }

  onChangeMaxNrParticipants(): void {
    this.showParticipantsLimit = !this.showParticipantsLimit;
  }

  formToObject(): object {
    return {
      title: this.eventForm.value.title,
      location: this.location,
      description: this.eventForm.value.description,
      visibility: this.eventForm.value.visibility,
      category: this.eventForm.value.category,
      minTrustLevel: this.eventForm.value.trustLevel,
      noMaxParticipants: this.eventForm.value.nrMaxParticipants,
      locationPoint: [this.eventForm.value.x, this.eventForm.value.y],
      startTime: this.addHoursMinsToDate(
        this.eventForm.value.startDate,
        this.eventForm.value.startTime
      ).toISOString(),
      endTime: this.addHoursMinsToDate(
        this.eventForm.value.endDate,
        this.eventForm.value.endTime
      ).toISOString(),
    };
  }

  onSubmitFinish(): void {
    this.listService.listUpdated$.next(null);
    this.dialog.close();
  }

  onSubmitAdd(): void {
    this.apiService.addEvent(this.formToObject())
      .subscribe(() => this.onSubmitFinish());
  }

  onSubmitUpdate(): void {
    this.apiService.updateEvent(this.data.event.id, this.formToObject())
      .subscribe(() => this.onSubmitFinish());
  }

  onSubmit(): void {
    if (this.data?.event) {
      this.onSubmitUpdate();
    } else {
      this.onSubmitAdd();
    }
  }

  optionSelectionChange(option: PlaceSuggestion, event: MatOptionSelectionChange): void {
    if (event.isUserInput) {
      this.chosenOption = option;
      this.autocompleteChanged(option);
    }
  }

  autocompleteChanged(data: any): void {
    latLng(data.data.lat, data.data.lon);
    this.location = data.fullAddress;
    this.eventForm.patchValue({
      x: data.data.lat,
      y: data.data.lon,
    });
    this.onNewLocation(data.data.lat, data.data.lon);
  }

  onNewLocation(lat, lng): void {
    if (this.newLocationMarker) {
      this.newLocationMarker.remove();
    }
    this.newLocationMarker = marker(latLng(lat, lng), {
      icon: icon({
        iconSize: [21, 37],
        iconAnchor: [10, 37],
        iconUrl: 'assets/pin.svg',
      }),
    });
    this.newLocationMarker.addTo(this.map);
  }

  onMapReady(leafletMap: Map): void {
    this.map = leafletMap;
    leafletMap.on('click', <LeafletMouseEvent>(e) => {
      this.eventForm.patchValue({
        x: e.latlng.lat,
        y: e.latlng.lng,
      });
      this.onNewLocation(e.latlng.lat, e.latlng.lng);
      this.updateLocationText(e.latlng.lat, e.latlng.lng);
    });
  }

  updateLocationText(lat: number, lng: number): void {
    this.geocodingService.getAddresBasedOnLocation(lat, lng).subscribe((value: any) => {
      const loc = value.features[0].properties.formatted;
      this.location = loc;
      this.inputFieldFormControl.patchValue(loc);

      // this.newLocationMarker = marker(latLng(e.latlng.lat, e.latlng.lng), {
      //   icon: icon({
      //     iconSize: [21, 37],
      //     iconAnchor: [10, 37],
      //     iconUrl: 'assets/pin.svg',
      //   }),
      // })

      // // leafletMap
      // this.newLocationMarker.addTo(leafletMap);

      // // leafletMap.addLayer(
      // //   [this.newLocationMarker
      // // );
    });
  }
}
