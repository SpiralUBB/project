import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { Invitation } from 'src/app/models/invitaion.interface';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-event-participants-confirm',
  templateUrl: './event-participants-confirm.component.html',
  styleUrls: ['./event-participants-confirm.component.scss'],
})
export class EventParticipantsConfirmComponent implements OnInit {
  @Input() eventId: string;
  constructor(private apiService: ApiService) {}

  invitations: Invitation[] = [];

  ngOnInit(): void {
    this.loadInvitations();
  }

  loadInvitations(): void {
    this.invitations = [];
    this.apiService.getEventInvitations(this.eventId).subscribe((response: any) => {
      const invitations = response.items;
      const keys = Object.keys(response.items);
      keys.forEach((key) => {
        if (invitations[key].status === 0) {
          this.invitations.push(invitations[key]);
        }
      });
    });
  }

  patchInvitaion(data: any): void {
    this.apiService.patchInvitationStatus(this.eventId, data.invitaionId, data.status).subscribe(
      () => {
        this.loadInvitations();
      }
    )
  }
}
