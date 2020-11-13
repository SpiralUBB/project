import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { AboutUsComponent } from './components/about-us/about-us/about-us.component';
import { DashboardComponent } from './components/dashboard/dashboard/dashboard.component';
import { LoginFormComponent } from './components/shared/login-form/login-form.component';
import { RegisterFormComponent} from './components/shared/register-form/register-form.component';
import { AuthGuardService } from './guards/auth-guard.service';

const routes: Routes = [
  {
    path: '',
    component: AppComponent,
    children: [
      { path: '', redirectTo: 'about-us', pathMatch: 'full' },
      { path: 'about-us', component: AboutUsComponent },
      { path: 'login', component: LoginFormComponent },
      { path: 'register', component: RegisterFormComponent},
      {
        path: 'dashboard',
        canActivate: [AuthGuardService],
        children: [
          {
            path: '',
            component: DashboardComponent,
          },
        ],
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
