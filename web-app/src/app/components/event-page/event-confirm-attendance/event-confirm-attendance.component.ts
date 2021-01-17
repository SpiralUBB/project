import { Component, Input, OnInit } from '@angular/core';
import { Invitation } from 'src/app/models/invitation.interface';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-event-confirm-attendance',
  templateUrl: './event-confirm-attendance.component.html',
  styleUrls: ['./event-confirm-attendance.component.scss'],
})
export class EventConfirmAttendanceComponent implements OnInit {
  @Input() eventId: string;
  invitations: Invitation[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadInvitations();
  }

  loadInvitations(): void {
    this.invitations = [];
    this.apiService.getEventInvitations(this.eventId).subscribe((response: any) => {
      const invitations = response.items;
      const keys = Object.keys(response.items);
      keys.forEach((key) => {
        if (invitations[key].status === 1) {
          this.invitations.push(invitations[key]);
        }
      });
    });
  }

  patchInvitation(data: any): void {
    this.apiService
      .patchAttendanceStatus(this.eventId, data.invitationId, data.status)
      .subscribe(() => {
        this.loadInvitations();
      });
  }
}
