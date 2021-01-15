import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { take } from 'rxjs/operators';
import { AppEvent } from 'src/app/models/app-event.interface';
import { Invitation } from 'src/app/models/invitaion.interface';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-event-participants-confirm',
  templateUrl: './event-participants-confirm.component.html',
  styleUrls: ['./event-participants-confirm.component.scss'],
})
export class EventParticipantsConfirmComponent implements OnInit, OnChanges {

  @Input() eventId: string;
  appEvent: AppEvent;

  constructor(private apiService: ApiService) { }

  private invitations: Invitation[];

  ngOnInit(): void {
    this.loadInvitations();
  }

  ngOnChanges(): void {
    this.apiService.getEventById(this.eventId).pipe(take(1)).subscribe(res => {
      this.appEvent = res;
    })
  }

  loadInvitations(): void {
    this.apiService.getEventInvitations(this.eventId).subscribe(
      (response: any) => {
        const invitations = response.items;
        const keys = Object.keys(response.items);
        keys.forEach(key => {
          if (invitations[key].staus === 0){
            this.invitations.push(invitations[key]);
          }
        });
      }
    );
  }

}
