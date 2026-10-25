
import {
  Component,
  computed,
  inject,
  signal
} from '@angular/core';

import {
  JobService
} from '../../services/job.service';

import {
  HttpErrorResponse
} from '@angular/common/http';

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

  private readonly jobService =
    inject(JobService);


  protected readonly jobs =
    signal<Job[]>([]);


  protected readonly loading =
    signal(true);


  protected readonly error =
    signal<string | null>(
      null
    );


  constructor() {

    this.loadJobs();

  }


  private loadJobs(): void {

    this.loading.set(
      true
    );

    this.error.set(
      null
    );


    this.jobService
      .getJobs()
      .subscribe({

        next: jobs => {

          this.jobs.set(
            jobs
          );

          this.loading.set(
            false
          );

        },


        error: (
          error: HttpErrorResponse
        ) => {

          console.error(
            'Failed to load jobs:',
            error
          );


          this.error.set(
            'Unable to load jobs.'
          );


          this.loading.set(
            false
          );

        }

      });

  }


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

    this.jobService
      .updateStatus(
        jobId,
        'SAVED'
      )
      .subscribe({

        next: updatedJob => {

          this.jobs.update(
            jobs =>
              jobs.map(
                job =>
                  job.id
                    === updatedJob.id
                    ? {
                        ...job,
                        status:
                          updatedJob.status
                      }
                    : job
              )
          );

        },


        error: error => {

          console.error(
            'Could not save job:',
            error
          );

        }

      });

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