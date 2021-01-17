import { Component, Input, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { User } from 'src/app/models/user';
import { ApiService } from 'src/app/services/api.service';
import { ParticipantFeedbackComponent } from '../participant-feedback/participant-feedback.component';

@Component({
  selector: 'app-participant-card',
  templateUrl: './participant-card.component.html',
  styleUrls: ['./participant-card.component.scss'],
})
export class ParticipantCardComponent implements OnInit {
  @Input() user: User;
  @Input() eventId: string;
  @Input() isOwner: boolean;

  hasFeedback = false;
  attendanceControl = new FormControl();
  invitationAttendStatuses: string[] = [];

  constructor(private dialog: MatDialog, private apiService: ApiService) {}

  ngOnInit(): void {
    this.apiService.getEventInvitationAttendStatuses().subscribe(res => {
      Object.values(res).forEach((status) => this.invitationAttendStatuses.push(String(status)));
    });
  }

  sendFeedback(): void {
    this.dialog.open(ParticipantFeedbackComponent, {
      data: {
        user: this.user,
        eventId: this.eventId,
      },
    });
  }
}
