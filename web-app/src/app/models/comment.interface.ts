import { User } from './user';

export interface AppComment {
  id: string;
  text: string;
  author: User;
  time: string;
}
