import { NumberValueAccessor } from '@angular/forms';
import { User } from './user';

export interface Invitation {
  attendStatus: number;
  attendStatusText: string;
  id: string;
  status: number;
  statusText: string;
  user?: User;
}
