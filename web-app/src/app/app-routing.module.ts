import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { EventFormComponent } from './components/event-form/event-form.component';
import { EventPageComponent } from './components/event-page/event-page.component';
import { EventsComponent } from './components/events/events.component';
import { LandingPageComponent } from './components/landing-page/landing-page.component';
import { MapComponent } from './components/map/map.component';
import { EventHistoryComponent } from './components/shared/event-history/event-history.component';
import { ProfileViewComponent } from './components/shared/profile-view/profile-view.component';
import { AuthGuardService } from './guards/auth-guard.service';

const routes: Routes = [
  { path: '', redirectTo: '/landing-page', pathMatch: 'full' },
  { path: 'landing-page', component: LandingPageComponent },
  {
    path: 'app',
    canActivate: [AuthGuardService],
    children: [
      {
        path: '',
        redirectTo: 'events',
        pathMatch: 'full',
      },
      {
        path: 'events',
        component: EventsComponent,
      },
      {
        path: 'map',
        component: MapComponent,
      },
      {
        path: 'event/:id',
        component: EventPageComponent,
      },
      {
        path: 'event-form/:id',
        component: EventFormComponent,
      },
      {
        path: 'profile',
        component: ProfileViewComponent,
      },
      {
        path: 'event-history',
        component: EventHistoryComponent,
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
