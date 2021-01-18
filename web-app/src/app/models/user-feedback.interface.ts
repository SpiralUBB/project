import { User } from './user';
import { AppEvent } from './app-event.interface';

export interface UserFeedback {
  fromUser: User;
  toUser: User;
  event: AppEvent;
  points: number;
  message: string;
}
