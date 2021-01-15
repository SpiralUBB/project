import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { ApiService } from 'src/app/services/api.service';
import { CategoryDialogComponent } from './category-dialog/category-dialog.component';

@Component({
  selector: 'app-filter-panel',
  templateUrl: './filter-panel.component.html',
  styleUrls: ['./filter-panel.component.scss'],
})
export class FilterPanelComponent implements OnInit {
  @Output() filterProps = new EventEmitter<any>();

  checkedCategories: string[] = [];
  categories: { id; name }[] = [];

  range = new FormGroup({
    start: new FormControl(),
    end: new FormControl(),
  });

  categoriesControl = new FormControl();

  constructor(
    public dialog: MatDialog,
    private apiService: ApiService
  ) { }

  ngOnInit(): void {
    this.getCategories();
  }

  getCategories(): void {
    this.apiService.getCategories().subscribe((eventsRes) => {
      Object.keys(eventsRes).forEach(key => {
        this.categories.push({ id: key, name: eventsRes[key] });
      });
    });
  }


  // openDialog(): void {
  //   const dialogConfig = new MatDialogConfig();

  //   dialogConfig.disableClose = true;
  //   dialogConfig.autoFocus = true;

  //   const dialogRef = this.dialog.open(CategoryDialogComponent, dialogConfig);

  //   dialogRef.afterClosed().subscribe((data) => (this.checkedCategories = data));
  // }

  filterEvents(): void {
    console.log('filterEvents');
    let supportTypeFilter = false;
    let supportDateFilter = false;
    let startDate = '';
    let endDate = '';

    console.log(this.categories);
    this.checkedCategories = this.categoriesControl.value;

    if (this.checkedCategories?.length > 0) {
      supportTypeFilter = true;
    }

    const date = {
      startDate: null,
      endDate: null,
    };

    if (this.range.value.start !== null) {
      supportDateFilter = true;
      const selectedDate = this.range.value.start;
      startDate =
        selectedDate.getFullYear() +
        '-' +
        (selectedDate.getMonth() + 1) +
        '-' +
        selectedDate.getDay();
      date.startDate = startDate;
    }

    if (this.range.value.end !== null) {
      supportDateFilter = true;
      const selectedDate = this.range.value.end;
      endDate =
        selectedDate.getFullYear() +
        '-' +
        (selectedDate.getMonth() + 1) +
        '-' +
        selectedDate.getDay();
      date.endDate = endDate;
    }

    this.filterProps.emit({
      supportTypeFilter,
      eventsTypeFilter: this.checkedCategories,
      supportDateFilter,
      eventsDateFilter: date,
    });
  }

  clearEvents(): void {
    console.log('clearEvents');
    this.checkedCategories = [];
    this.range.value.start = null;
    this.range.value.end = null;
    this.filterProps.emit({
      supportTypeFilter: false,
      eventsTypeFilter: [],
      supportDateFilter: false,
      eventsDateFilter: {},
    });
  }

  deleteCategory(name: string): void {
    console.log(name);
    for (let i = 0; i < this.checkedCategories.length; i++) {
      if (this.checkedCategories[i] === name) {
        this.checkedCategories.splice(i, 1);
      }
    }
  }
}
