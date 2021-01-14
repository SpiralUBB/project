import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import {MatDialog} from "@angular/material/dialog";
import {EventFormComponent} from "../event-form/event-form.component";

@Component({
  selector: 'app-events',
  templateUrl: './events.component.html',
  styleUrls: ['./events.component.scss']
})
export class EventsComponent implements OnInit {

  constructor(private apiService: ApiService,
              private dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.apiService.getCurrentUser().subscribe((res) => {
      console.log(res);
    })
  }

  openEventFormDialog() {
    const dialogRef = this.dialog.open(EventFormComponent);
  }
}
