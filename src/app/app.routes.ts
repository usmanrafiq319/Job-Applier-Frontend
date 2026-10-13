import { Routes } from '@angular/router';
import { AppShell } from './layout/app-shell/app-shell';

export const routes: Routes = [

  {
    path: '',
    component: AppShell,

    children: [

      {
        path: '',
        pathMatch: 'full',
        redirectTo: 'dashboard'
      },


      {
        path: 'dashboard',

        loadComponent: () =>
          import(
            './features/dashboard/dashboard'
          )
          .then(
            module =>
              module.Dashboard
          )
      },


      {
        path: 'profile',

        loadComponent: () =>
          import(
            './features/profile/profile'
          )
          .then(
            module =>
              module.Profile
          )
      },


      {
        path: 'jobs/analyze',

        loadComponent: () =>
          import(
            './features/job-analyzer/job-analyzer'
          )
          .then(
            module =>
              module.JobAnalyzer
          )
      },


      {
        path: 'jobs',

        loadComponent: () =>
          import(
            './features/jobs/jobs'
          )
          .then(
            module =>
              module.Jobs
          )
      },


      {
        path: 'jobs/:id',

        loadComponent: () =>
          import(
            './features/job-details/job-details'
          )
          .then(
            module =>
              module.JobDetails
          )
      },


      {
        path: 'outreach',

        loadComponent: () =>
          import(
            './features/outreach/outreach'
          )
          .then(
            module =>
              module.Outreach
          )
      },
      {
        path: 'applications',

        loadComponent: () =>
          import(
            './features/applications/applications'
          )
          .then(
            module =>
              module.Applications
          )
      }

    ]
  },

  {
    path: '**',
    redirectTo: 'dashboard'
  }

];
