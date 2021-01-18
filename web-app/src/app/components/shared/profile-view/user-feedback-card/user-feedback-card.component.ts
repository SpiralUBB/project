import { Component, Input, OnInit } from '@angular/core';
import { UserFeedback } from '../../../../models/user-feedback.interface';

@Component({
  selector: 'app-user-feedback-card',
  templateUrl: './user-feedback-card.component.html',
  styleUrls: ['./user-feedback-card.component.scss'],
})
export class UserFeedbackCardComponent implements OnInit {
  @Input() feedback: UserFeedback;

  absoluteFeedbackPoints: number;

  ngOnInit(): void {
    this.absoluteFeedbackPoints = (this.feedback.points + 6) / 12 * 5;
  }
}
