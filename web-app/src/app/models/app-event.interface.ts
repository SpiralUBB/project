import { User } from "./user";

// Cause Event already exists in angular
export interface AppEvent {
  id: string;
  category: number;
  categoryText: string;
  startTime: string;
  endTime: string;
  title: string;
  description: string;
  owner: EventOwner;
  visibility: number;
  visibilityText: string;
  location?: string;
  locationPoints?: [x: number, y: number];
  isLimitedDetails?: boolean;
  isUnlimitedParticipants?: boolean;
  locationPointsRadiusMeters?: number;
  noMaxParticipants: number;
}

export interface EventOwner {
  firstName: string;
  lastName: string;
  username: string;
  points: number;
  trustLevel: number;
}
