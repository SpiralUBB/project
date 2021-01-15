import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class HttpErrorInterceptorService implements HttpInterceptor {
  constructor(private snackbar: MatSnackBar) {}

  private static isHttpErrorResponse(error): error is HttpErrorResponse {
    return error instanceof HttpErrorResponse;
  }

  intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {
        let errorMsg = '';
        if (error.error instanceof ErrorEvent) {
          console.log('this is client side error');
          errorMsg = `Error: ${error.error.message}`;
        } else {
          console.log('this is server side error');
          errorMsg = `Error Code: ${error.status},  Message: ${error.message}`;
        }
        console.log(errorMsg);
        const backendCustomError = error.error;
        console.log(backendCustomError);
        errorMsg = errorMsg.concat(
          `\n${backendCustomError.code}\n${backendCustomError.message}`
        );
        const snackBarRef = this.snackbar.open(errorMsg, null, {
          duration: 5000,
        });
        return throwError(errorMsg);
      })
    ) as Observable<HttpEvent<any>>;
  }
}
