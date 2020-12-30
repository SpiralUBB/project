import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { NavigationStart, Router, RouterEvent } from '@angular/router';
import { filter, take, tap } from 'rxjs/operators';
import { AppEvent } from 'src/app/models/app-event.interface';

@Component({
  selector: 'app-marker-popup',
  templateUrl: './marker-popup.component.html',
  styleUrls: ['./marker-popup.component.scss'],
})
export class MarkerPopupComponent implements OnInit {
  constructor(
    private dialogRef: MatDialogRef<MarkerPopupComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { event: AppEvent },
    private router: Router
  ) {}

  event: AppEvent;

  ngOnInit(): void {
    this.event = this.data.event;

    this.router.events
      .pipe(
        filter((event: RouterEvent) => event instanceof NavigationStart),
        tap(() => this.dialogRef.close()),
        take(1)
      )
      .subscribe();
  }
}