import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Invitation } from 'src/app/models/invitation.interface';
import { User } from 'src/app/models/user';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-event-participant-confirm-card',
  templateUrl: './event-participant-confirm-card.component.html',
  styleUrls: ['./event-participant-confirm-card.component.scss'],
})
export class EventParticipantConfirmCardComponent {
  @Input() invitation: Invitation;
  @Output() patchInvitation = new EventEmitter<any>();
  constructor(private apiService: ApiService) {}

  acceptInvitation(): void {
    const data = {
      invitationId: this.invitation.id,
      status: 'accepted',
    };
    this.patchInvitation.emit(data);
  }

  declineInvitation(): void {
    const data = {
      invitationId: this.invitation.id,
      status: 'denied',
    };
    this.patchInvitation.emit(data);
  }
}
