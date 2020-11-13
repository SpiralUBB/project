import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MaterialModule } from './material-module';
import { LoginFormComponent } from './components/shared/login-form/login-form.component';
import { HttpClientModule, HttpResponse, HTTP_INTERCEPTORS } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AuthService } from './services/auth.service';
import { HttpResponseParserService } from './services/http-response-parser.service';
import { AboutUsComponent } from './components/about-us/about-us/about-us.component';
import { DashboardComponent } from './components/dashboard/dashboard/dashboard.component';
import { RegisterFormComponent } from './components/shared/register-form/register-form.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginFormComponent,
    AboutUsComponent,
    DashboardComponent,
    RegisterFormComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    MaterialModule,
    HttpClientModule
  ],
  providers: [AuthService, {
    provide: HTTP_INTERCEPTORS,
    useClass: HttpResponseParserService,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
