import { Component, Input, OnInit } from '@angular/core';
import { AppEvent } from 'src/app/models/app-event.interface';

@Component({
  selector: 'app-event-card',
  templateUrl: './event-card.component.html',
  styleUrls: ['./event-card.component.scss']
})
export class EventCardComponent implements OnInit {

  @Input() event: AppEvent;

  constructor() { }

  ngOnInit(): void {
  }

}
