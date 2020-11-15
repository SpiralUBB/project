//Cause Event already exists in angular
export interface AppEvent {
  category: number;
  categoryText: string;
  date: string;
  description: string;
  id: string;
  location?: string;
  locationPoints: [x: number, y: number];
}
