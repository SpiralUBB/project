import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormControl, FormControlName, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { latLng, tileLayer, Map } from 'leaflet';
import { Observable } from 'rxjs';
import { filter, map, take } from 'rxjs/operators';
import { ApiService } from 'src/app/services/api.service';

interface CheckBoxSlection {
  value: number | string;
  viewValue: number | string;
}

@Component({
  selector: 'app-event-form',
  templateUrl: './event-form.component.html',
  styleUrls: ['./event-form.component.scss'],
})

export class EventFormComponent implements OnInit {
  eventId$: Observable<string>;
  categories: CheckBoxSlection[] = [];
  trustLevelOptions: CheckBoxSlection[] = [];
  show: boolean = false;
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
    nrMaxParticipants: new FormControl(0),
    textarea: new FormControl('')
  });

  constructor(
    private activatedRoute: ActivatedRoute,
    private apiService: ApiService,
    private dialog: MatDialogRef<EventFormComponent>
  ) { }

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

    this.apiService.getCategories().pipe(take(1)).subscribe(
        (res) => this.addEventsCategories(res)
    );

    this.apiService.getCurrentUser().pipe(take(1)).subscribe(
        (currentUser) => this.addTrusLevelOptions(currentUser.trustLevel)
    )
  }

  addEventsCategories(categroiesType: any){
    Object.keys(categroiesType).forEach(key => {
        const category = {
            value: key,
            viewValue: key
        }
        this.categories.push(category);
    });
  }

  addTrusLevelOptions(currentUserTrustLevel: number){
    const noMinRequierd = {
        value: 0,
        viewValue: "Any trust level"
    };
    this.trustLevelOptions.push(noMinRequierd);

    for(let i = 1; i<currentUserTrustLevel; i++){
        const checkBoxOption = {
            value: i,
            viewValue: i
        }
        this.trustLevelOptions.push(checkBoxOption);
    }
  }

  onChangeMaxNrParticipants(): void {
    if(this.show) {
      this.show = false;
    }
    else {
      this.show = true;
    }
  }

  @ViewChild('textarea')
  private textarea;

  onMouseOver() {
    if(this.textarea.nativeElement != document.activeElement){
      this.textarea.nativeElement.style.border = "2px solid black";
    }
  }

  onMouseLeave() {
    this.textarea.nativeElement.style.border = "1px solid rgb(128, 128, 128)";
  }

  onSubmit() {
    // TODO: Use EventEmitter with form value
    console.warn(this.eventForm.value);
    this.apiService.addEvent({
      title: this.eventForm.value.title,
      location: this.eventForm.value.location,
      description: this.eventForm.value.textarea,
      visibility: this.eventForm.value.visibility,
      category: this.eventForm.value.category,
      min_trust_level: this.eventForm.value.trustLevel,
      no_max_participants: this.eventForm.value.nrMaxParticipants,
      start_time: this.eventForm.value.startDate + "T" + this.eventForm.value.startTime,
      end_time: this.eventForm.value.endDate + "T" + this.eventForm.value.endTime
    }).subscribe(() => {
      this.dialog.close();
    });
  }

  onMapReady(map: Map) {
    console.log("map ready")
    map.on('click', <LeafletMouseEvent>(e) => { console.log(e.latlng) });
  }
}
