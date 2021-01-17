import { Component, Inject, Input } from '@angular/core';
import { NgModel } from '@angular/forms';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { User } from 'src/app/models/user';
import { ApiService } from 'src/app/services/api.service';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-participant-feedback',
  templateUrl: './participant-feedback.component.html',
  styleUrls: ['./participant-feedback.component.scss'],
})
export class ParticipantFeedbackComponent {
  rateFirstQuestion = 3;
  rateSecondQuestion = 3;
  rateThirdQuestion = 3;
  textareaInput: string;

  constructor(
    private authService: AuthService,
    private apiService: ApiService,
    @Inject(MAT_DIALOG_DATA) public data: { user: User; eventId: string }
  ) {}

  submitFeedback(): void {
    this.apiService
      .putFeedback(
        this.data.user.username,
        this.data.eventId,
        this.rateFirstQuestion + this.rateSecondQuestion + this.rateThirdQuestion - 9,
        this.textareaInput
      )
      .subscribe();
  }
}
