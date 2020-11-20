import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { filter, map } from 'rxjs/operators';

@Component({
  selector: 'app-event-page',
  templateUrl: './event-page.component.html',
  styleUrls: ['./event-page.component.scss'],
})
export class EventPageComponent implements OnInit {
  constructor(private activatedRoute: ActivatedRoute) {}

  public eventId$: Observable<number>;
  private id: number;

  ngOnInit(): void {
    //daca navighezi pe un url nou unde difera doar id-ul nu se incarca pagina noua, doar se emite o alta valoare in observable
    this.eventId$ = this.activatedRoute.params.pipe(
      filter((params) => !!params.id),
      map((params) => params.id)
    );

    //Ii dai subscribe aici daca ai nevoie de el in ts
    this.eventId$.subscribe((id) => {
      this.id = id;
      console.log(this.id);
    });
  }
}
