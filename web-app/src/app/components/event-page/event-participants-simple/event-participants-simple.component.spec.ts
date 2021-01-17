import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventParticipantsSimpleComponent } from './event-participants-simple.component';

describe('EventParticipantsComponent', () => {
  let component: EventParticipantsSimpleComponent;
  let fixture: ComponentFixture<EventParticipantsSimpleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EventParticipantsSimpleComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EventParticipantsSimpleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
