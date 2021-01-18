import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subscription } from 'rxjs';
import { GeocodingFeatureProperties } from '../models/geocoding-feature-properties.interface';

@Injectable({
  providedIn: 'root',
})
export class GeocodingService {
  private requestSub: Subscription;

  constructor(private http: HttpClient) {}

  getApiCall(text: string): any {
    const url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${text}&limit=5&apiKey=71682df212584412aaeb1623f2b46cda`;
    return this.http.get(url);
  }

  generateSuggestions(text: string): void {
    const url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${text}&limit=5&apiKey=71682df212584412aaeb1623f2b46cda`;

    if (this.requestSub) {
      this.requestSub.unsubscribe();
    }

    this.requestSub = this.http.get(url).subscribe(
      (data: GeoJSON.FeatureCollection) => {
        const placeSuggestions = data.features.map((feature) => {
          const properties: GeocodingFeatureProperties = feature.properties as GeocodingFeatureProperties;

          return {
            shortAddress: this.generateShortAddress(properties),
            fullAddress: this.generateFullAddress(properties),
            data: properties,
          };
        });

        return placeSuggestions;
      },
      (err) => {
        console.log(err);
      }
    );
  }

  generateShortAddress(properties: GeocodingFeatureProperties): string {
    let shortAddress = properties.name ?? properties.city;

    if (!shortAddress && properties.street && properties.housenumber) {
      // name is not set for buildings
      shortAddress = `${properties.street} ${properties.housenumber}`;
    }

    shortAddress +=
      properties.postcode && properties.city ? `, ${properties.postcode}-${properties.city}` : '';
    shortAddress +=
      !properties.postcode && properties.city && properties.city !== properties.name
        ? `, ${properties.city}`
        : '';
    shortAddress +=
      properties.country && properties.country !== properties.name ? `, ${properties.country}` : '';

    return shortAddress;
  }

  generateFullAddress(properties: GeocodingFeatureProperties): string {
    console.log(properties);
    let fullAddress = properties.name;
    fullAddress += properties.street ? `, ${properties.street}` : '';
    fullAddress += properties.housenumber ? ` ${properties.housenumber}` : '';
    fullAddress +=
      properties.postcode && properties.city ? `, ${properties.postcode}-${properties.city}` : '';
    fullAddress +=
      !properties.postcode && properties.city && properties.city !== properties.name
        ? `, ${properties.city}`
        : '';
    fullAddress += properties.state ? `, ${properties.state}` : '';
    fullAddress +=
      properties.country && properties.country !== properties.name ? `, ${properties.country}` : '';
    return fullAddress;
  }

  getAddresBasedOnLocation(lat: number, lng: number): Observable<any> {
    const url = `https://api.geoapify.com/v1/geocode/reverse?lat=${lat}&lon=${lng}&apiKey=1b48259b810e48ddb151889f9ea58db0`;
    return this.http.get(url);
  }
}
