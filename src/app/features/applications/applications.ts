import {
  Component,
  computed,
  signal
} from '@angular/core';

import {
  DatePipe
} from '@angular/common';

import {
  Application,
  ApplicationStatus
} from '../../models/application.model';

import {
  StatCard
} from '../../shared/components/stat-card/stat-card';


type ApplicationStatusFilter =
  | 'ALL'
  | ApplicationStatus;


@Component({
  selector: 'app-applications',

  imports: [
    DatePipe,
    StatCard
  ],

  templateUrl: './applications.html',

  styleUrl: './applications.css'
})
export class Applications {

  /*
   * Temporary frontend data.
   *
   * Later:
   *
   * private readonly applicationService =
   *   inject(ApplicationService);
   *
   * this.applicationService
   *   .getApplications()
   *   .subscribe(...)
   */
  protected readonly applications =
    signal<Application[]>([

      {
        id: 'application-1',

        jobId: 'job-1',

        jobTitle:
          'Junior .NET Developer',

        company:
          'Tech Solutions',

        location:
          'Lahore, Pakistan',

        matchScore:
          88,

        status:
          'SENT',

        contactName:
          'Hiring Team',

        contactEmail:
          'careers@techsolutions.com',

        outreachId:
          'draft-1',

        appliedAt:
          '2026-10-04T15:00:00Z',

        lastUpdatedAt:
          '2026-10-04T15:00:00Z',

        notes:
          'Applied through personalized email outreach.'
      },


      {
        id: 'application-2',

        jobId: 'job-2',

        jobTitle:
          '.NET Backend Developer',

        company:
          'NovaSoft',

        location:
          'Lahore, Pakistan',

        matchScore:
          74,

        status:
          'READY',

        contactName:
          'Recruitment Team',

        contactEmail:
          'jobs@novasoft.com',

        outreachId:
          'draft-2',

        lastUpdatedAt:
          '2026-10-05T09:00:00Z',

        notes:
          'Email approved but not yet sent.'
      },


      {
        id: 'application-3',

        jobId: 'job-3',

        jobTitle:
          'AI Backend Intern',

        company:
          'AI Labs',

        location:
          'Remote, Pakistan',

        matchScore:
          82,

        status:
          'REPLIED',

        contactEmail:
          'careers@ailabs.com',

        appliedAt:
          '2026-10-02T11:00:00Z',

        lastUpdatedAt:
          '2026-10-05T12:20:00Z',

        notes:
          'Recruiter replied and requested availability.'
      },


      {
        id: 'application-4',

        jobId: 'job-4',

        jobTitle:
          'Angular Developer',

        company:
          'Digital House',

        location:
          'Lahore, Pakistan',

        matchScore:
          69,

        status:
          'INTERVIEW',

        contactName:
          'HR Team',

        contactEmail:
          'hr@digitalhouse.com',

        appliedAt:
          '2026-10-01T09:30:00Z',

        lastUpdatedAt:
          '2026-10-05T14:00:00Z',

        notes:
          'Technical interview scheduled.'
      }

    ]);


  protected readonly searchTerm =
    signal('');


  protected readonly statusFilter =
    signal<ApplicationStatusFilter>(
      'ALL'
    );


  protected readonly selectedApplication =
    signal<Application | null>(
      null
    );


  protected readonly filteredApplications =
    computed(() => {

      const search =
        this.searchTerm()
          .trim()
          .toLowerCase();


      const status =
        this.statusFilter();


      return this.applications()
        .filter(
          application => {

            const matchesSearch =
              !search ||
              application.jobTitle
                .toLowerCase()
                .includes(search) ||
              application.company
                .toLowerCase()
                .includes(search) ||
              (
                application.location ?? ''
              )
                .toLowerCase()
                .includes(search);


            const matchesStatus =
              status === 'ALL' ||
              application.status === status;


            return (
              matchesSearch &&
              matchesStatus
            );

          }
        );

    });


  protected readonly sentCount =
    computed(
      () =>
        this.applications()
          .filter(
            application =>
              [
                'SENT',
                'REPLIED',
                'INTERVIEW',
                'REJECTED',
                'OFFER'
              ].includes(
                application.status
              )
          )
          .length
    );


  protected readonly replyCount =
    computed(
      () =>
        this.applications()
          .filter(
            application =>
              [
                'REPLIED',
                'INTERVIEW',
                'OFFER'
              ].includes(
                application.status
              )
          )
          .length
    );


  protected readonly interviewCount =
    computed(
      () =>
        this.applications()
          .filter(
            application =>
              application.status ===
              'INTERVIEW'
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
      ).value as ApplicationStatusFilter;


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


  protected updateStatus(
    applicationId: string,
    event: Event
  ): void {

    const status =
      (
        event.target as
          HTMLSelectElement
      ).value as ApplicationStatus;


    this.applications.update(
      applications =>
        applications.map(
          application =>
            application.id ===
            applicationId
              ? {
                  ...application,

                  status,

                  appliedAt:
                    status === 'SENT' &&
                    !application.appliedAt
                      ? new Date()
                          .toISOString()
                      : application.appliedAt,

                  lastUpdatedAt:
                    new Date()
                      .toISOString()
                }
              : application
        )
    );


    const selected =
      this.selectedApplication();


    if (
      selected?.id ===
      applicationId
    ) {

      const updated =
        this.applications()
          .find(
            application =>
              application.id ===
              applicationId
          );


      this.selectedApplication.set(
        updated ?? null
      );

    }

  }


  protected openDetails(
    application: Application
  ): void {

    this.selectedApplication.set(
      application
    );

  }


  protected closeDetails(): void {

    this.selectedApplication.set(
      null
    );

  }


  protected updateNotes(
    event: Event
  ): void {

    const selected =
      this.selectedApplication();


    if (!selected) {

      return;

    }


    const notes =
      (
        event.target as
          HTMLTextAreaElement
      ).value;


    this.applications.update(
      applications =>
        applications.map(
          application =>
            application.id ===
            selected.id
              ? {
                  ...application,
                  notes,
                  lastUpdatedAt:
                    new Date()
                      .toISOString()
                }
              : application
        )
    );


    this.selectedApplication.update(
      current =>
        current
          ? {
              ...current,
              notes
            }
          : null
    );

  }


  protected getStatusClass(
    status: ApplicationStatus
  ): string {

    switch (status) {

      case 'DRAFT':

        return 'badge badge-neutral';


      case 'READY':

        return 'badge badge-warning';


      case 'SENT':

        return 'badge badge-info';


      case 'REPLIED':

        return 'badge badge-success';


      case 'INTERVIEW':

        return 'badge badge-success';


      case 'OFFER':

        return 'badge badge-success';


      case 'REJECTED':

        return 'badge badge-danger';

    }

  }


  protected getMatchClass(
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


  protected statusLabel(
    status: ApplicationStatus
  ): string {

    return status
      .replaceAll(
        '_',
        ' '
      );

  }

}