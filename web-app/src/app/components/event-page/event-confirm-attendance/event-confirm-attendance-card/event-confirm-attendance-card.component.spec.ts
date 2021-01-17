import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventConfirmAttendanceCardComponent } from './event-confirm-attendance-card.component';

describe('EventConfirmAttendanceCardComponent', () => {
  let component: EventConfirmAttendanceCardComponent;
  let fixture: ComponentFixture<EventConfirmAttendanceCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EventConfirmAttendanceCardComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EventConfirmAttendanceCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
