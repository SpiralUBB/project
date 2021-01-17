import { User } from './user';

export interface AppEvent {
  id: string;
  category: number;
  categoryText: string;
  startTime: string;
  endTime: string;
  title: string;
  description: string;
  owner: User;
  visibility: number;
  visibilityText: string;
  location?: string;
  locationPoints?: [x: number, y: number];
  isLimitedDetails?: boolean;
  isUnlimitedParticipants?: boolean;
  locationPointsRadiusMeters?: number;
  noMaxParticipants: number;
  noParticipants?: number;
  minTrustLevel?: number;
}
