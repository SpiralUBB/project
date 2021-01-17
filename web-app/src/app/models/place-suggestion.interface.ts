import { GeocodingFeatureProperties } from './geocoding-feature-properties.interface';

export interface PlaceSuggestion {
  shortAddress: string;
  fullAddress: string;
  data: GeocodingFeatureProperties;
}
