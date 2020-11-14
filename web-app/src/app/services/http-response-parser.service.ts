import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from "rxjs/operators";
import { isObject } from 'util';

@Injectable({
  providedIn: 'root'
})
export class HttpResponseParserService implements HttpInterceptor {

  private apiBasePath = 'http://localhost:5000/api/v1';

  constructor() { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const newReq = req.clone({
      url: this.apiBasePath + req.url,
      body: this.remapKeysToSnakeCase(req.body),
      withCredentials: true
    })

    return next.handle(newReq).pipe(
      map((event: HttpEvent<any>) => {
        if (event instanceof HttpResponse) {
          let camelCaseObject = this.remapKeysToCamelCase(event.body);
          const modEvent = event.clone({ body: camelCaseObject });

          return modEvent;
        }
        
      })
    )
  }

  private remapKeysToCamelCase(o: object) {
    if (o !== null && typeof o === 'object') {
      const n = {};

      Object.keys(o)
        .forEach((k) => {
          n[this.toCamel(k)] = this.remapKeysToCamelCase(o[k]);
        });
  
      return n;
    } else if (Array.isArray(o)) {
      return o.map((i) => {
        return this.toCamel(i);
      });
    }
    return o;
  }


  private toCamel(toParse: string) {
    console.log(toParse);
    // const toReturn = toParse.replace('/([-_][a-z])/g',
    //   (group) => group.toUpperCase()
    //     .replace('-', '')
    //     .replace('_', ''));
    const toReturn = toParse.split('_').map((x, i) => ((i > 0) ? x[0].toUpperCase() : x[0]) + x.slice(1)).join('');
    console.log(toReturn);
    return toReturn;
  }


  private remapKeysToSnakeCase(o: object) {
    if (o !== null && typeof o === 'object') {
      const n = {};

      Object.keys(o)
        .forEach((k) => {
          n[this.toSnake(k)] = this.remapKeysToSnakeCase(o[k]);
        });
  
      return n;
    } else if (Array.isArray(o)) {
      return o.map((i) => {
        return this.toSnake(i);
      });
    }
    return o;
  }


  private toSnake(toParse: string) {
    console.log(toParse);
    // const toReturn = toParse.replace('/([-_][a-z])/g',
    //   (group) => group.toUpperCase()
    //     .replace('-', '')
    //     .replace('_', ''));
    const toReturn = toParse.replace(/(?:^|\.?)([A-Z])/g, function (x,y){return "_" + y.toLowerCase()}).replace(/^_/, "")
    console.log(toReturn);
    return toReturn;
  }
}
