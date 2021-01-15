import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Invitation } from 'src/app/models/invitaion.interface';

@Component({
  selector: 'app-event-confirm-attendance-card',
  templateUrl: './event-confirm-attendance-card.component.html',
  styleUrls: ['./event-confirm-attendance-card.component.scss']
})
export class EventConfirmAttendanceCardComponent implements OnInit {

  @Input() invitation: Invitation;
  @Output() patchInvitation = new EventEmitter<any>();
  shouldDisplayStatus : boolean;
  constructor() { 

  }

  ngOnInit(): void {
    this.shouldDisplayStatus =  this.invitation.attendStatus !== 0;
  }
  
  confirmAttendence(): void {
    let data = {
      invitaionId: this.invitation.id,
      status: "attended"
    };
    this.patchInvitation.emit(data);
  }
  
  declineAttendence(): void {
    let data = {
      invitaionId: this.invitation.id,
      status: "missed"
    };
    this.patchInvitation.emit(data);
  }
}
