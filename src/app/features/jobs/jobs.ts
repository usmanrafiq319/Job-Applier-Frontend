
import {
  Component,
  computed,
  inject,
  signal
} from '@angular/core';

import {
  DatePipe
} from '@angular/common';

import {
  Router
} from '@angular/router';

import {
  Job,
  JobStatus
} from '../../models/job.model';


type JobStatusFilter =
  | 'ALL'
  | JobStatus;


@Component({
  selector: 'app-jobs',

  imports: [
    DatePipe
  ],

  templateUrl: './jobs.html',

  styleUrl: './jobs.css'
})
export class Jobs {

  private readonly router =
    inject(Router);


  /*
   * Later:
   *
   * private readonly jobService =
   *   inject(JobService);
   *
   * this.jobService
   *   .getJobs()
   *   .subscribe(...)
   */


  protected readonly jobs =
    signal<Job[]>([

      {
        id: 'job-1',

        title:
          'Junior .NET Developer',

        company:
          'Tech Solutions',

        location:
          'Lahore, Pakistan',

        description:
          'Looking for a junior developer with ASP.NET Core, C#, Angular, SQL and REST API experience.',

        employmentType:
          'FULL_TIME',

        experienceRequired:
          '0-2 years',

        status:
          'HIGH_MATCH',

        matchScore:
          88,

        createdAt:
          '2026-10-05T10:00:00Z'
      },


      {
        id: 'job-2',

        title:
          '.NET Backend Developer',

        company:
          'NovaSoft',

        location:
          'Lahore, Pakistan',

        description:
          'Backend development role using .NET, PostgreSQL, REST APIs, Docker and Azure.',

        employmentType:
          'FULL_TIME',

        experienceRequired:
          '1-2 years',

        status:
          'ANALYZED',

        matchScore:
          74,

        createdAt:
          '2026-10-04T08:30:00Z'
      },


      {
        id: 'job-3',

        title:
          'AI Backend Intern',

        company:
          'AI Labs',

        location:
          'Remote, Pakistan',

        description:
          'AI backend internship working with FastAPI, LLMs, vector search, LangChain and RAG.',

        employmentType:
          'INTERNSHIP',

        experienceRequired:
          'Entry Level',

        status:
          'HIGH_MATCH',

        matchScore:
          82,

        createdAt:
          '2026-10-03T13:00:00Z'
      },


      {
        id: 'job-4',

        title:
          'Angular Developer',

        company:
          'Digital House',

        location:
          'Lahore, Pakistan',

        description:
          'Frontend-focused Angular opportunity requiring Angular, TypeScript, Tailwind and REST API integration.',

        employmentType:
          'FULL_TIME',

        experienceRequired:
          '1 year',

        status:
          'ANALYZED',

        matchScore:
          69,

        createdAt:
          '2026-10-02T11:15:00Z'
      },


      {
        id: 'job-5',

        title:
          'Cloud .NET Engineer',

        company:
          'Enterprise Cloud',

        location:
          'Lahore, Pakistan',

        description:
          'Experienced .NET developer required with Azure, Docker, Kubernetes and cloud-native development.',

        employmentType:
          'FULL_TIME',

        experienceRequired:
          '3+ years',

        status:
          'LOW_MATCH',

        matchScore:
          46,

        createdAt:
          '2026-10-01T09:45:00Z'
      }

    ]);


  protected readonly searchTerm =
    signal('');


  protected readonly statusFilter =
    signal<JobStatusFilter>(
      'ALL'
    );


  protected readonly filteredJobs =
    computed(() => {

      const search =
        this.searchTerm()
          .trim()
          .toLowerCase();


      const status =
        this.statusFilter();


      return this.jobs()
        .filter(
          job => {

            const matchesSearch =
              !search ||
              job.title
                .toLowerCase()
                .includes(search) ||
              job.company
                .toLowerCase()
                .includes(search) ||
              (
                job.location ?? ''
              )
                .toLowerCase()
                .includes(search);


            const matchesStatus =
              status === 'ALL' ||
              job.status === status;


            return (
              matchesSearch &&
              matchesStatus
            );

          }
        );

    });


  protected readonly highMatchCount =
    computed(
      () =>
        this.jobs()
          .filter(
            job =>
              (
                job.matchScore ??
                0
              ) >= 80
          )
          .length
    );


  protected searchChanged(
    event: Event
  ): void {

    const value =
      (
        event.target as
          HTMLInputElement
      ).value;


    this.searchTerm.set(
      value
    );

  }


  protected statusChanged(
    event: Event
  ): void {

    const value =
      (
        event.target as
          HTMLSelectElement
      ).value as JobStatusFilter;


    this.statusFilter.set(
      value
    );

  }


  protected clearFilters(): void {

    this.searchTerm.set('');

    this.statusFilter.set(
      'ALL'
    );

  }


  protected saveJob(
    jobId: string
  ): void {

    this.jobs.update(
      jobs =>
        jobs.map(
          job =>
            job.id === jobId
              ? {
                  ...job,
                  status:
                    'SAVED'
                }
              : job
        )
    );

  }


  protected analyzeAnotherJob():
    void {

    this.router.navigate([
      '/jobs/analyze'
    ]);

  }


  protected getMatchBadgeClass(
    score?: number
  ): string {

    if (!score) {

      return 'badge badge-neutral';

    }


    if (score >= 80) {

      return 'badge badge-success';

    }


    if (score >= 60) {

      return 'badge badge-warning';

    }


    return 'badge badge-danger';

  }


  protected getStatusBadgeClass(
    status: JobStatus
  ): string {

    switch (status) {

      case 'HIGH_MATCH':

        return 'badge badge-success';


      case 'ANALYZED':
      case 'SAVED':

        return 'badge badge-info';


      case 'LOW_MATCH':
      case 'REJECTED':

        return 'badge badge-danger';


      case 'APPLIED':

        return 'badge badge-success';


      case 'FOUND':

        return 'badge badge-neutral';

    }

  }


  protected statusLabel(
    status: JobStatus
  ): string {

    return status
      .replaceAll(
        '_',
        ' '
      );

  }

  protected viewDetails(
  jobId: string
): void {

  this.router.navigate([
    '/jobs',
    jobId
  ]);

}

}