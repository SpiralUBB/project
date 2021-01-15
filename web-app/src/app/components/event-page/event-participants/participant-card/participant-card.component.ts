import { Component, Input, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { User } from 'src/app/models/user';
import { ParticipantFeedbackComponent } from '../participant-feedback/participant-feedback.component';

@Component({
  selector: 'app-participant-card',
  templateUrl: './participant-card.component.html',
  styleUrls: ['./participant-card.component.scss'],
})
export class ParticipantCardComponent implements OnInit {
  @Input() user: User;
  @Input() canLeaveFeedback = true;
  @Input() eventId: string;

  constructor(
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {}
  
  sendFeedback() {
    this.dialog.open(ParticipantFeedbackComponent, {
      data: {
        user: this.user,
        eventId: this.eventId
      }
    })
  }
}
