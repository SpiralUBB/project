import { Component, Input, OnInit } from '@angular/core';
import { User } from 'src/app/models/user';

@Component({
  selector: 'app-participant-card',
  templateUrl: './participant-card.component.html',
  styleUrls: ['./participant-card.component.scss']
})
export class ParticipantCardComponent implements OnInit {

  @Input() user: User;
  @Input() canLeaveFeedback = true;
  constructor() { }

  ngOnInit(): void {
  }

}
