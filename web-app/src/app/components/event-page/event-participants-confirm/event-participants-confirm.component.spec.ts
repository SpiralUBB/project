import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventParticipantsConfirmComponent } from './event-participants-confirm.component';

describe('EventParticipantsConfirmComponent', () => {
  let component: EventParticipantsConfirmComponent;
  let fixture: ComponentFixture<EventParticipantsConfirmComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EventParticipantsConfirmComponent ],
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EventParticipantsConfirmComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
