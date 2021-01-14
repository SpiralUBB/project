import { Component, OnInit } from '@angular/core';
import { AppEvent } from 'src/app/models/app-event.interface';
import { ApiService } from 'src/app/services/api.service';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-event-history',
  templateUrl: './event-history.component.html',
  styleUrls: ['./event-history.component.scss']
})
export class EventHistoryComponent implements OnInit {

  eventsCreated: AppEvent[] = [];
  eventsParticipated: AppEvent[] = [];

  constructor(private apiService: ApiService,private authService: AuthService) { }

  ngOnInit(): void {
    this.apiService.getAllEvents().subscribe((eventsRes) => {
      Object.keys(eventsRes.items).forEach(key => {
        if(eventsRes.items[key].owner.username==this.authService.currentUserValue.username)
          this.eventsCreated.push(eventsRes.items[key])
      })
    });
    this.apiService.getAttendedEvents().subscribe((eventsRes) =>{
      Object.keys(eventsRes.items).forEach(key => {
        this.eventsParticipated.push(eventsRes.items[key])
      })
    });
  }

}
