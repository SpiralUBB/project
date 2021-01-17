import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventConfirmAttendanceComponent } from './event-confirm-attendance.component';

describe('EventConfirmAttendanceComponent', () => {
  let component: EventConfirmAttendanceComponent;
  let fixture: ComponentFixture<EventConfirmAttendanceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EventConfirmAttendanceComponent ],
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EventConfirmAttendanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
