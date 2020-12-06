import { Component, OnInit } from '@angular/core';
import { AppEvent } from 'src/app/models/app-event.interface';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-event-list',
  templateUrl: './event-list.component.html',
  styleUrls: ['./event-list.component.scss']
})
export class EventListComponent implements OnInit {

  events: AppEvent[] = [];
  
  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.apiService.getAllEvents().subscribe((eventsRes) => {
      Object.keys(eventsRes.items).forEach(key => {
        this.events.push(eventsRes.items[key])
      })
    });
  }

  onFilterProps(data: any){
    console.log("onFilterProps");
    let categories=data["eventsTypeFilter"];
    let startDate=null,endDate=null;
    startDate=data["eventsDateFilter"]["startDate"];
    endDate=data["eventsDateFilter"]["endDate"];
    this.apiService.getFilterEvents(categories,startDate,endDate).subscribe((eventsRes)=>{
      this.events=[];
      Object.keys(eventsRes.items).forEach(key => {
        this.events.push(eventsRes.items[key])
      })
    })
  }


}
