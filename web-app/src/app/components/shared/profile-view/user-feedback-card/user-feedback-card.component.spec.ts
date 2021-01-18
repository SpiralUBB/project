import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserFeedbackCardComponent } from './user-feedback-card.component';

describe('ParticipantCardComponent', () => {
  let component: UserFeedbackCardComponent;
  let fixture: ComponentFixture<UserFeedbackCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [UserFeedbackCardComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UserFeedbackCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
