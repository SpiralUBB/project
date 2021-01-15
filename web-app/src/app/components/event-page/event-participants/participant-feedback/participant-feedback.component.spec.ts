import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ParticipantFeedbackComponent } from './participant-feedback.component';

describe('ParticipantFeedbackComponent', () => {
  let component: ParticipantFeedbackComponent;
  let fixture: ComponentFixture<ParticipantFeedbackComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ParticipantFeedbackComponent ],
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ParticipantFeedbackComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
