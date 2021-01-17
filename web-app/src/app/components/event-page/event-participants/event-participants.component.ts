import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { of } from 'rxjs';
import { mergeMap } from 'rxjs/operators';
import { ApiResponse } from 'src/app/models/api-response.interface';
import { Invitation } from 'src/app/models/invitation.interface';
import { User } from 'src/app/models/user';
import { ApiService } from 'src/app/services/api.service';
import { ParticipantFeedbackComponent } from './participant-feedback/participant-feedback.component';

@Component({
  selector: 'app-event-participants',
  templateUrl: './event-participants.component.html',
  styleUrls: ['./event-participants.component.scss'],
})
export class EventParticipantsComponent implements OnInit, OnChanges {
  @Input() eventId: string;
  @Input() isOwner: boolean;

  participants: User[];

  constructor(
    private apiService: ApiService,
    private dialog: MatDialog
  ) { }

  ngOnInit(): void {}

  ngOnChanges(): void {
    this.apiService.getEventInvitations(this.eventId).subscribe((invitations: ApiResponse<Invitation>) => {
      console.log(invitations);
      this.participants = invitations.items
        .filter(invitation => invitation.status === 1)
        .map(invitation => invitation.user);
      console.log(this.participants);
    });
  }

  leaveFeedback(): void {
    this.dialog.open(ParticipantFeedbackComponent);
  }
}
