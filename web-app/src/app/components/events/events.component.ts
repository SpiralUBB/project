import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { MatDialog } from '@angular/material/dialog';
import { EventFormComponent } from '../event-form/event-form.component';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-events',
  templateUrl: './events.component.html',
  styleUrls: ['./events.component.scss'],
})
export class EventsComponent implements OnInit {

  isLoggedIn: boolean;

  constructor(
    private apiService: ApiService, 
    private dialog: MatDialog, 
    private router: Router,
    private authService: AuthService
  ) {}
  

  ngOnInit(): void {
    // this.apiService.getCurrentUser().subscribe((res) => {
    // });
    this.authService.isLoggedIn().subscribe(isLoggedIn => this.isLoggedIn = isLoggedIn);
  }

  openEventFormDialog(): void {
    const dialogRef = this.dialog.open(EventFormComponent);
    dialogRef.afterClosed().subscribe(() => {
      this.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
        this.router.navigate(['/events']);
      });
    });
  }
}
