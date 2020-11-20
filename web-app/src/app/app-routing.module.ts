import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { EventPageComponent } from './components/event-page/event-page.component';
import { EventsComponent } from './components/events/events.component';
import { LandingPageComponent } from './components/landing-page/landing-page.component';
import { MapComponent } from './components/map/map.component';
import { LoginFormComponent } from './components/shared/login-form/login-form.component';
import { RegisterFormComponent } from './components/shared/register-form/register-form.component';
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
    ],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
