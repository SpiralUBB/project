import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-event-participants',
  templateUrl: './event-participants.component.html',
  styleUrls: ['./event-participants.component.scss']
})
export class EventParticipantsComponent implements OnInit {

  @Input() eventId: string;
  constructor() { }

  ngOnInit(): void {
  }

}
