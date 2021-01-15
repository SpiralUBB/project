import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-category-dialog',
  templateUrl: './category-dialog.component.html',
  styleUrls: ['./category-dialog.component.scss'],
})
export class CategoryDialogComponent implements OnInit {

  categories: {name, checked}[] = [];

  constructor(private apiService: ApiService, private dialogRef: MatDialogRef<CategoryDialogComponent>) { }

  ngOnInit(): void {
    this.getCategories();
  }

  getCategories(): void {
    this.apiService.getCategories().subscribe((eventsRes) => {
      Object.keys(eventsRes).forEach(key => {
        this.categories.push({name: key, checked: false});
      });
    });
  }


  save(): void {
    const values = this.categories
              .filter(opt => opt.checked)
              .map(opt => opt.name);
    this.dialogRef.close(values);
}

  close(): void {
      this.dialogRef.close();
  }
}
