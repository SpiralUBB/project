import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormControl, FormControlName } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { filter, map } from 'rxjs/operators';

interface Category {
  value: string;
  viewValue: string;
}

@Component({
  selector: 'app-event-form',
  templateUrl: './event-form.component.html',
  styleUrls: ['./event-form.component.scss'],
})

export class EventFormComponent implements OnInit {
  public eventId$: Observable<string>;

  constructor(private activatedRoute: ActivatedRoute) {}

  ngOnInit(): void {
    this.eventId$ = this.activatedRoute.params.pipe(
      filter((params) => !!params.id),
      map((params) => params.id)
    );
  }

  categories: Category[] = [
    {value: 'music', viewValue: 'Music'},
    {value: 'party', viewValue: 'Party'},
    {value: 'beuta', viewValue: 'Beuta'}
  ];

  show: boolean = false;
  f(): void {
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

  eventForm = new FormGroup({
    title: new FormControl(''),
    location: new FormControl(''),
    startDate: new FormControl(''),
    endDate: new FormControl(''),
    visibility: new FormControl(''),
    category: new FormControl(''),
    trustLevel: new FormControl(''),
    nrMaxParticipants: new FormControl(''),
    textarea: new FormControl('')
  });

  onSubmit() {
    // TODO: Use EventEmitter with form value
    console.warn(this.eventForm.value);
  }
}
