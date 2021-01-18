import { Component, Inject, LOCALE_ID, NgZone, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { GeoJSON, icon, latLng, LatLng, LatLngLiteral, Map, Layer, LeafletMouseEvent, marker, tileLayer } from 'leaflet';
import { Subject, Subscription } from 'rxjs';
import { take } from 'rxjs/operators';
import { ApiService } from 'src/app/services/api.service';
import * as moment from 'moment';
import { PlaceSuggestion } from 'src/app/models/place-suggestion.interface';
import { MatOptionSelectionChange } from '@angular/material/core';
import { GeocodingService } from 'src/app/services/geocoding.service';
import { GeocodingFeatureProperties } from 'src/app/models/geocoding-feature-properties.interface';
import { ListService } from 'src/app/services/list.service';
import { AppEvent } from 'src/app/models/app-event.interface';
import { MatSnackBar } from '@angular/material/snack-bar';

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
    private zone: NgZone,
    private activatedRoute: ActivatedRoute,
    private apiService: ApiService,
    private dialog: MatDialogRef<EventFormComponent>,
    private geocodingService: GeocodingService,
    private listService: ListService,
    @Inject(MAT_DIALOG_DATA) public data: { event: AppEvent },
    @Inject(LOCALE_ID) public locale: string,
    private snackService: MatSnackBar
  ) {}

  searchOptions: Subject<PlaceSuggestion[]> = new Subject<PlaceSuggestion[]>();
  private valueChangesSub: Subscription;
  private userInputTimeout: number;
  private location: string;
  private chosenOption: PlaceSuggestion;
  private requestSub: Subscription;

  private map: Map = null;
  mapZoom = 7;
  mapCenter: LatLng = latLng({
    lat: 0,
    lng: 0,
  });
  mapCenterMarker = marker([0, 0], {
    icon: icon({
      iconSize: [21, 37],
      iconAnchor: [10, 37],
      iconUrl: 'assets/pin.svg',
    }),
  });
  mapLayers: Layer[] = [
    tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 20,
    }),
    this.mapCenterMarker,
  ];

  categories: SelectOption[] = [];
  visibilities: SelectOption[] = [];
  trustLevelOptions: SelectOption[] = [];
  showParticipantsLimit = false;
  eventForm = new FormGroup({
    title: new FormControl(null, [Validators.required]),
    location: new FormControl(null, [Validators.required]),
    startDate: new FormControl(null, [Validators.required]),
    endDate: new FormControl(null, [Validators.required]),
    startTime: new FormControl(null, [Validators.required]),
    endTime: new FormControl(null, [Validators.required]),
    visibility: new FormControl(null, [Validators.required]),
    category: new FormControl(null, [Validators.required]),
    trustLevel: new FormControl(null, [Validators.required]),
    x: new FormControl(null, [Validators.required]),
    y: new FormControl(null, [Validators.required]),
    noMaxParticipants: new FormControl(),
    description: new FormControl(null, [Validators.required]),
  });

  private generateSuggestions(text: string): void {
    if (this.requestSub) {
      this.requestSub.unsubscribe();
    }

    this.requestSub = this.geocodingService.getApiCall(text).subscribe(
      (data: GeoJSON.FeatureCollection) => {
        const placeSuggestions = data.features.map((feature) => {
          const properties = feature.properties as GeocodingFeatureProperties;

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

  dateAddHours(date: Date = new Date(), hours: number = 0): Date {
    const newDate = new Date(date);
    newDate.setHours(date.getHours() + hours);
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
    let initialPatchData;
    let initialLatLng;

    if (this.data?.event) {
      initialPatchData = {
        title: this.data.event.title,
        startDate: this.utcStringToLocalDateTime(this.data.event.startTime),
        endDate: this.utcStringToLocalDateTime(this.data.event.endTime),
        x: this.data.event.locationPoints[0],
        y: this.data.event.locationPoints[1],
        noMaxParticipants: this.data.event.noMaxParticipants,
        description: this.data.event.description,
        location: this.data.event.location,
      };

      initialLatLng = {
        lat: this.data.event.locationPoints[0],
        lng: this.data.event.locationPoints[1],
      };

      if (this.data.event.noMaxParticipants > 0) {
        this.showParticipantsLimit = true;
      }
    } else {
      initialPatchData = {
        title: '',
        startDate: this.dateAddHours(undefined, 1),
        endDate: this.dateAddHours(undefined, 2),
        x: 0,
        y: 0,
        noMaxParticipants: 0,
        description: '',
      };

      initialLatLng = {
        lat: 0,
        lng: 0,
      };

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
          this.setLatLon({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
        });
      }
    }

    Object.assign(initialPatchData, {
      startTime: this.getTimeFormat(initialPatchData.startDate),
      endTime: this.getTimeFormat(initialPatchData.endDate),
    });

    this.eventForm.patchValue(initialPatchData);
    this.setLatLon(initialLatLng);

    this.valueChangesSub = this.eventForm
      .get('location')
      .valueChanges.subscribe((value) => {
        if (this.userInputTimeout) {
          clearTimeout(this.userInputTimeout);
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

  onChangeNoMaxParticipants(event: any): void {
    this.showParticipantsLimit = !this.showParticipantsLimit;
    if (!this.showParticipantsLimit) {
      this.eventForm.patchValue({
        noMaxParticipants: 0,
      });
    }
  }

  formAsObject(): object {
    return {
      title: this.eventForm.value.title,
      location: this.eventForm.value.location,
      description: this.eventForm.value.description,
      visibility: this.eventForm.value.visibility,
      category: this.eventForm.value.category,
      minTrustLevel: this.eventForm.value.trustLevel,
      noMaxParticipants: this.eventForm.value.noMaxParticipants,
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
    this.listService.eventUpdated$.next(null);
    this.dialog.close();
  }

  onSubmitAdd(): void {
    this.apiService.addEvent(this.formAsObject())
      .subscribe(
        () => this.onSubmitFinish(),
        (err) => {
          this.snackService.open(err?.error?.message ?? 'Something went wrong...', null, {duration: 4000});
        }
      );
  }

  onSubmitUpdate(): void {
    this.apiService.updateEvent(this.data.event.id, this.formAsObject())
      .subscribe(
        () => this.onSubmitFinish(),
        (err) => {
          this.snackService.open(err?.error?.message ?? 'Something went wrong...', null, {duration: 4000});
        }
    );
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

  setLatLon(lg: LatLngLiteral): void {
    this.mapCenter.lat = lg.lat;
    this.mapCenter.lng = lg.lng;

    this.eventForm.patchValue({
      x: lg.lat,
      y: lg.lng,
    });

    this.mapCenterMarker.setLatLng(lg);

    if (this.map) {
      this.map.panTo(lg);
    }
  }

  autocompleteChanged(data: any): void {
    this.setLatLon({
      lat: data.data.lat,
      lng: data.data.lon,
    });
  }

  onMapReady(map: Map): void {
    console.log('ready');
    this.map = map;
  }

  onMapClick(e: LeafletMouseEvent): void {
    this.zone.run(() => {
      this.setLatLon(e.latlng);
      this.updateLocationText(e.latlng);
    });
  }

  updateLocationText(lg: LatLngLiteral): void {
    this.geocodingService.getAddresBasedOnLocation(lg.lat, lg.lng)
      .subscribe((value: any) => {
        this.eventForm.patchValue({
          location: value.features[0].properties.formatted,
        });
    });
  }
}
