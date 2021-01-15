import { Component, Input, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-event-confirm-attendance',
  templateUrl: './event-confirm-attendance.component.html',
  styleUrls: ['./event-confirm-attendance.component.scss']
})
export class EventConfirmAttendanceComponent implements OnInit {

  @Input() eventId: string;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
  }

}
