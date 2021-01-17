import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ApiResponse } from 'src/app/models/api-response.interface';
import { Invitation } from 'src/app/models/invitation.interface';
import { ApiService } from 'src/app/services/api.service';
import { ParticipantFeedbackComponent } from './participant-feedback/participant-feedback.component';
import { User } from '../../../models/user';

@Component({
  selector: 'app-event-participants',
  templateUrl: './event-participants.component.html',
  styleUrls: ['./event-participants.component.scss'],
})
export class EventParticipantsComponent implements OnInit, OnChanges {
  @Input() eventId: string;
  @Input() isOwner: boolean;
  @Input() user: User;

  invitations: Invitation[];

  constructor(private apiService: ApiService, private dialog: MatDialog) {}

  ngOnInit(): void {}

  ngOnChanges(): void {
    this.apiService
      .getEventInvitations(this.eventId)
      .subscribe((invitations: ApiResponse<Invitation>) => {
        this.invitations = invitations.items;
      });
  }

  leaveFeedback(): void {
    this.dialog.open(ParticipantFeedbackComponent);
  }
}
