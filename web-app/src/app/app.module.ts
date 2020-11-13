import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MaterialModule } from './material-module';
import { LoginFormComponent } from './components/shared/login-form/login-form.component';
import {
  HttpClientModule,
  HttpResponse,
  HTTP_INTERCEPTORS,
} from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AuthService } from './services/auth.service';
import { HttpResponseParserService } from './services/http-response-parser.service';
import { HttpErrorInterceptorService } from './services/http-error-interceptor.service';
import { ErrorSnackbarComponent } from './components/shared/error-snackbar/error-snackbar.component';
import { NavbarComponent } from './components/shared/navbar/navbar.component';
import { EventsComponent } from './components/events/events.component';
import { LandingPageComponent } from './components/landing-page/landing-page.component';
import { SidenavComponent } from './components/shared/sidenav/sidenav.component';
import { SidenavContentComponent } from './components/shared/sidenav/sidenav-content/sidenav-content.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginFormComponent,
    ErrorSnackbarComponent,
    NavbarComponent,
    EventsComponent,
    LandingPageComponent,
    SidenavComponent,
    SidenavContentComponent,
  ],
  imports: [
    MaterialModule,
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
  ],
  providers: [
    AuthService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttpResponseParserService,
      multi: true,
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttpErrorInterceptorService,
      multi: true,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
