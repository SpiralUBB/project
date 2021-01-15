import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  HttpResponse,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { camelKeys, snakeKeys } from 'js-convert-case/lib';

@Injectable({
  providedIn: 'root',
})
export class HttpResponseParserService implements HttpInterceptor {
  private apiBasePath = 'http://localhost:5000/api/v1';

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const newReq = req.clone({
      url: this.apiBasePath + req.url,
      // body: this.remapKeysToSnakeCase(req.body),
      body: this.objectToSnake(req.body),
      withCredentials: true,
    });

    return next.handle(newReq).pipe(
      map((event: HttpEvent<any>) => {
        if (event instanceof HttpResponse) {
          // const camelCaseObject = this.remapKeysToCamelCase(event.body);
          // return event.clone({ body: camelCaseObject });
          return event.clone({
            body: this.objectToCamel(event.body),
          });
        }
      })
    );
  }

  // private remapKeysToCamelCase(o: object): object {
  //   if (o !== null && typeof o === 'object') {
  //     const n = {};

  //     Object.keys(o).forEach((k) => {
  //       n[this.toCamel(k)] = this.remapKeysToCamelCase(o[k]);
  //     });

  //     return n;
  //   } else if (Array.isArray(o)) {
  //     return o.map((i) => {
  //       return this.toCamel(i);
  //     });
  //   }
  //   return o;
  // }

  // private toCamel(toParse: string): string {
  //   return toParse
  //     .split('_')
  //     .map((x, i) => (i > 0 ? x[0].toUpperCase() : x[0]) + x.slice(1))
  //     .join('');
  // }

  // private remapKeysToSnakeCase(o: object): object {
  //   if (o !== null && typeof o === 'object') {
  //     const n = {};

  //     Object.keys(o).forEach((k) => {
  //       n[this.toSnake(k)] = this.remapKeysToSnakeCase(o[k]);
  //     });

  //     return n;
  //   } else if (Array.isArray(o)) {
  //     return o.map((i) => {
  //       return this.toSnake(i);
  //     });
  //   }
  //   return o;
  // }

  // private toSnake(toParse: string): string {
  //   return toParse
  //     .replace(/(?:^|\.?)([A-Z])/g, (x, y) => {
  //       return '_' + y.toLowerCase();
  //     })
  //     .replace(/^_/, '');
  // }

  objectToSnake(data: any): any {
    return snakeKeys(data, {
      recursive: true,
      recursiveInArray: true,
    });
  }

  objectToCamel(data: any): any {
    return camelKeys(data, {
      recursive: true,
      recursiveInArray: true,
    });
  }
}
