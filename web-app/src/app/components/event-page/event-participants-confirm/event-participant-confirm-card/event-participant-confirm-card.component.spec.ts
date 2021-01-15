import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventParticipantConfirmCardComponent } from './event-participant-confirm-card.component';

describe('EventParticipantConfirmCardComponent', () => {
  let component: EventParticipantConfirmCardComponent;
  let fixture: ComponentFixture<EventParticipantConfirmCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EventParticipantConfirmCardComponent ],
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EventParticipantConfirmCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
