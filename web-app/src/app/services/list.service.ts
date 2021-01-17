import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';

@Injectable()
export class ListService {
  constructor(

  ) { }
  
  listUpdated$ = new Subject();
}
