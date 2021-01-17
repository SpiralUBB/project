import { Component, OnInit } from '@angular/core';
import { AppEvent } from 'src/app/models/app-event.interface';
import { ApiService } from 'src/app/services/api.service';
import { ListService } from 'src/app/services/list.service';

@Component({
  selector: 'app-event-list',
  templateUrl: './event-list.component.html',
  styleUrls: ['./event-list.component.scss'],
})
export class EventListComponent implements OnInit {
  events: AppEvent[] = [];
  categories: string[];
  startDate: string;
  endDate: string;

  constructor(private apiService: ApiService, private listService: ListService) {}

  ngOnInit(): void {
    const startDate = new Date().toISOString();
    this.getFilterEvents(null, startDate, null);
    this.listService.listUpdated$.subscribe(() => {
      this.getFilterEvents(this.categories, this.startDate, this.endDate);
    });
  }

  onFilterProps(data: any): void {
    this.categories = data.eventsTypeFilter;
    this.startDate = data.eventsDateFilter.startDate;
    this.endDate = data.eventsDateFilter.endDate;
    
    this.getFilterEvents(this.categories, this.startDate, this.endDate);
  }

  getFilterEvents(categories, startDate, endDate): void {
    this.apiService.getFilterEvents(categories, startDate, endDate).subscribe((eventsRes) => {
      this.events = [];
      Object.keys(eventsRes.items).forEach((key) => {
        this.events.push(eventsRes.items[key]);
      });
    });
  }


}
