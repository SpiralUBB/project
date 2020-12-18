import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormControl, FormControlName, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { filter, map } from 'rxjs/operators';
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

  eventForm = new FormGroup({
    title: new FormControl('', [Validators.required]),
    location: new FormControl('', [Validators.required]),
    startDate: new FormControl('', [Validators.required]),
    endDate: new FormControl('', [Validators.required]),
    visibility: new FormControl('', [Validators.required]),
    category: new FormControl('', [Validators.required]),
    trustLevel: new FormControl('', [Validators.required]),
    nrMaxParticipants: new FormControl(''),
    textarea: new FormControl('')
  });

  constructor(private activatedRoute: ActivatedRoute,
    private apiService: ApiService) {}

  ngOnInit(): void {
    this.eventId$ = this.activatedRoute.params.pipe(
      filter((params) => !!params.id),
      map((params) => params.id)
    );

    this.apiService.getCategories().subscribe(
        (res) => this.addEventsCategories(res)
    );

    this.apiService.getCurrentUser().subscribe(
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
  }
}
