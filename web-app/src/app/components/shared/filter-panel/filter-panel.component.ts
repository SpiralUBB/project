import { Component, EventEmitter, Inject, NgModule, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatDialog, MatDialogConfig, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from 'src/app/services/api.service';
import { CategoryDialogComponent } from './category-dialog/category-dialog.component';


@Component({
  selector: 'app-filter-panel',
  templateUrl: './filter-panel.component.html',
  styleUrls: ['./filter-panel.component.scss']
})
export class FilterPanelComponent implements OnInit {
  @Output() filterProps=new EventEmitter<any>();


  checkedCategories: String[]=[];

  range = new FormGroup({
    start: new FormControl(),
    end: new FormControl()
  });

  constructor(private apiService: ApiService,public dialog: MatDialog) { }

  ngOnInit(): void {

  }

  
  openDialog() {
    const dialogConfig = new MatDialogConfig();

    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    
    const dialogRef = this.dialog.open(CategoryDialogComponent, dialogConfig);

    dialogRef.afterClosed().subscribe(
        data => this.checkedCategories=data
    );    
  }

  filterEvents(){
    console.log("filterEvents");
    let supportTypeFilter=false,supportDateFilter=false;
    let startDate="",endDate="";
    if(this.checkedCategories.length>0){
      supportTypeFilter=true;
    }
    let date={};
    if(this.range.value.start!=null){
      supportDateFilter=true;
      let date=this.range.value.start;
      startDate=date.getFullYear()+"-"+date.getMonth()+"-"+date.getDay();
      date["startDate"]=startDate;
    }
    if(this.range.value.end!=null){
      supportDateFilter=true;
      let date=this.range.value.end;
      endDate=date.getFullYear()+"-"+date.getMonth()+"-"+date.getDay();
      date["endDate"]=endDate;
    }
    this.filterProps.emit({
      "supportTypeFilter":supportTypeFilter,
      "eventsTypeFilter": this.checkedCategories,
      "supportDateFilter":supportDateFilter,
      "eventsDateFilter":date
    });
  }

  clearEvents(){
    console.log("clearEvents");
    this.checkedCategories=[];
    this.range.value.start=null;
    this.range.value.end=null;
    this.filterProps.emit({
      "supportTypeFilter":false,
      "eventsTypeFilter": [],
      "supportDateFilter": false,
      "eventsDateFilter": {},
    })
  }
}



