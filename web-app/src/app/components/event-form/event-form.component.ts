import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { filter, map } from 'rxjs/operators';

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
}
