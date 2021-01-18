import { Component, Input, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ApiService } from 'src/app/services/api.service';
import { ParticipantFeedbackComponent } from '../participant-feedback/participant-feedback.component';
import { Invitation } from '../../../../models/invitation.interface';

interface SelectValue {
  value: number;
  viewValue: string;
}

@Component({
  selector: 'app-participant-card',
  templateUrl: './participant-card.component.html',
  styleUrls: ['./participant-card.component.scss'],
})
export class ParticipantCardComponent implements OnInit {
  @Input() invitation: Invitation;
  @Input() eventId: string;
  @Input() isOwner: boolean;
  @Input() isOwnInvitation: boolean;

  invitationStatuses: SelectValue[] = [];
  invitationAttendStatuses: SelectValue[] = [];

  updatedStatus: number | string;
  statusDisabled = true;

  updatedAttendStatus: number | string;
  attendStatusDisabled = true;

  constructor(private dialog: MatDialog, private apiService: ApiService) {}

  ngOnInit(): void {
    this.apiService.getEventInvitationAttendStatuses().subscribe(res => {
      Object.entries(res).forEach((keyValue) => {
        this.invitationAttendStatuses.push({
          value: Number(keyValue[0]),
          viewValue: keyValue[1],
        });
        this.updatedStatus = this.invitation.status;
        this.statusDisabled = false;
      });
    });

    this.apiService.getEventInvitationStatuses().subscribe(res => {
      Object.entries(res).forEach((keyValue) => {
        this.invitationStatuses.push({
          value: Number(keyValue[0]),
          viewValue: keyValue[1],
        });
        this.updatedAttendStatus = this.invitation.attendStatus;
        this.attendStatusDisabled = false;
      });
    });
  }

  onStatusChange(): void {
    this.statusDisabled = true;
    this.apiService.patchInvitationStatus(
      this.eventId,
      this.invitation.id,
      this.updatedStatus
    ).subscribe(() => {
      this.statusDisabled = false;
    });
  }

  onAttendStatusChange(): void {
    this.attendStatusDisabled = true;
    this.apiService.patchInvitationAttendanceStatus(
      this.eventId,
      this.invitation.id,
      this.updatedAttendStatus
    ).subscribe(() => {
      this.attendStatusDisabled = false;
    });
  }

  sendFeedback(): void {
    this.dialog.open(ParticipantFeedbackComponent, {
      data: {
        user: this.invitation.user,
        eventId: this.eventId,
      },
    });
  }
}
