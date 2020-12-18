import { InterpolationConfig } from "@angular/compiler";

export interface EventCreationModel {
    title: string,
    location: string,
    locationPoints: [],
    stratTime: string,
    endTime: string,
    description: string,
    visibility: string,
    category: string,
    minTrustLevel: number,
    noMaxParticipants: number
}