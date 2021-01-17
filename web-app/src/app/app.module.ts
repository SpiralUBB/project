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
import { CommonModule } from '@angular/common';

import { RegisterFormComponent } from './components/shared/register-form/register-form.component';
import { HttpErrorInterceptorService } from './services/http-error-interceptor.service';
import { ErrorSnackbarComponent } from './components/shared/error-snackbar/error-snackbar.component';
import { NavbarComponent } from './components/shared/navbar/navbar.component';
import { EventsComponent } from './components/events/events.component';
import { LandingPageComponent } from './components/landing-page/landing-page.component';
import { SidenavComponent } from './components/shared/sidenav/sidenav.component';
import { SidenavContentComponent } from './components/shared/sidenav/sidenav-content/sidenav-content.component';
import { NavigationService } from './services/navigation.service';
import { MapComponent } from './components/map/map.component';
import { LeafletModule } from '@asymmetrik/ngx-leaflet';
import { EventCardComponent } from './components/shared/event-card/event-card.component';
import { EventListComponent } from './components/shared/event-list/event-list.component';
import { EventPageComponent } from './components/event-page/event-page.component';
import { ProfileFormComponent } from './components/shared/profile-form/profile-form.component';
import { EventCommentsComponent } from './components/event-page/event-comments/event-comments.component';
import { CommentCardComponent } from './components/event-page/event-comments/comment-card/comment-card.component';
import { EventParticipantsComponent } from './components/event-page/event-participants/event-participants.component';
import { ParticipantCardComponent } from './components/event-page/event-participants/participant-card/participant-card.component';
import { EventDetailsComponent } from './components/event-page/event-details/event-details.component';
import { FilterPanelComponent } from './components/shared/filter-panel/filter-panel.component';
import { ParticipantFeedbackComponent } from './components/event-page/event-participants/participant-feedback/participant-feedback.component';
import { EventFormComponent } from './components/event-form/event-form.component';
import { EventParticipantsConfirmComponent } from './components/event-page/event-participants-confirm/event-participants-confirm.component';
import { EventParticipantConfirmCardComponent } from './components/event-page/event-participants-confirm/event-participant-confirm-card/event-participant-confirm-card.component';
import { CategoryDialogComponent } from './components/shared/filter-panel/category-dialog/category-dialog.component';
import { MarkerPopupComponent } from './components/map/marker-popup/marker-popup.component';
import { ProfileViewComponent } from './components/shared/profile-view/profile-view.component';
import { EventHistoryComponent } from './components/shared/event-history/event-history.component';
import { DatePipe } from '@angular/common';
import { EventsUpcomingComponent } from './components/shared/events-upcoming/events-upcoming.component';
import { EventConfirmAttendanceComponent } from './components/event-page/event-confirm-attendance/event-confirm-attendance.component';
import { EventConfirmAttendanceCardComponent } from './components/event-page/event-confirm-attendance/event-confirm-attendance-card/event-confirm-attendance-card.component';
import { BarRatingModule } from 'ngx-bar-rating';

@NgModule({
  declarations: [
    AppComponent,
    LoginFormComponent,
    RegisterFormComponent,
    ErrorSnackbarComponent,
    NavbarComponent,
    EventsComponent,
    LandingPageComponent,
    SidenavComponent,
    SidenavContentComponent,
    MapComponent,
    EventCardComponent,
    EventListComponent,
    EventPageComponent,
    ProfileFormComponent,
    EventCommentsComponent,
    CommentCardComponent,
    EventParticipantsComponent,
    ParticipantCardComponent,
    EventDetailsComponent,
    FilterPanelComponent,
    ParticipantFeedbackComponent,
    EventFormComponent,
    EventParticipantsConfirmComponent,
    EventParticipantConfirmCardComponent,
    CategoryDialogComponent,
    MarkerPopupComponent,
    CategoryDialogComponent,
    ProfileViewComponent,
    EventHistoryComponent,
    EventsUpcomingComponent,
    EventConfirmAttendanceComponent,
    EventConfirmAttendanceCardComponent,
  ],
  imports: [
    CommonModule,
    MaterialModule,
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    LeafletModule,
    BarRatingModule,
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
    NavigationService,
    DatePipe,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
