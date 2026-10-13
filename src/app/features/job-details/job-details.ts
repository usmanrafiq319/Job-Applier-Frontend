import {
  Component,
  inject,
  signal
} from '@angular/core';

import {
  ActivatedRoute,
  Router
} from '@angular/router';

import {
  DatePipe
} from '@angular/common';

import {
  JobDetailsData,
  MatchRecommendation
} from '../../models/job-analysis.model';


@Component({
  selector: 'app-job-details',

  imports: [
    DatePipe
  ],

  templateUrl: './job-details.html',

  styleUrl: './job-details.css'
})
export class JobDetails {

  private readonly route =
    inject(ActivatedRoute);

  private readonly router =
    inject(Router);


  protected readonly loading =
    signal(true);


  protected readonly jobDetails =
    signal<JobDetailsData | null>(
      null
    );


  protected readonly notFound =
    signal(false);


  /*
   * Temporary frontend mock data.
   *
   * Later:
   *
   * this.jobService
   *   .getJob(id)
   *
   * OR ideally:
   *
   * GET /api/v1/jobs/{id}
   *
   * returning JobDetailsData
   */

  private readonly mockJobs:
    Record<string, JobDetailsData> = {

    'job-1': {

      job: {

        id: 'job-1',

        title:
          'Junior .NET Developer',

        company:
          'Tech Solutions',

        location:
          'Lahore, Pakistan',

        description:
          `We are looking for a Junior .NET Developer
with hands-on knowledge of ASP.NET Core, C#, Angular,
SQL, REST APIs and modern web development practices.

The candidate will work with our backend and frontend
teams to build business applications and APIs.`,

        jobUrl:
          'https://example.com/jobs/dotnet',

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


      analysis: {

        jobId:
          'job-1',

        matchScore:
          88,

        recommendation:
          'STRONG_MATCH',

        summary:
          `This role strongly aligns with your .NET full-stack background.
Your ASP.NET Core, Angular, SQL, REST API and SignalR experience
covers most of the important requirements.`,

        matchedSkills: [

          'ASP.NET Core',

          'C#',

          'Angular',

          'SQL',

          'REST APIs',

          'Entity Framework Core'

        ],

        missingSkills: [

          'Azure'

        ],

        requirements: [

          {
            skill:
              'ASP.NET Core',

            required:
              true,

            matched:
              true
          },

          {
            skill:
              'C#',

            required:
              true,

            matched:
              true
          },

          {
            skill:
              'Angular',

            required:
              true,

            matched:
              true
          },

          {
            skill:
              'REST APIs',

            required:
              true,

            matched:
              true
          },

          {
            skill:
              'Azure',

            required:
              false,

            matched:
              false
          }

        ],

        relevantExperience: [

          {
            id:
              'experience-1',

            type:
              'EXPERIENCE',

            title:
              '.NET Full-Stack Internship',

            content:
              `Worked with ASP.NET Core, Angular,
REST APIs, SQL databases and real-time application features.`,

            similarityScore:
              0.93
          },

          {
            id:
              'project-1',

            type:
              'PROJECT',

            title:
              'Full-Stack E-Commerce',

            content:
              `Built an ASP.NET Core and Angular
e-commerce application with JWT authentication,
SignalR chat, PostgreSQL and Cloudflare R2.`,

            similarityScore:
              0.89
          }

        ],

        analyzedAt:
          '2026-10-05T10:05:00Z'

      }

    },


    'job-2': {

      job: {

        id:
          'job-2',

        title:
          '.NET Backend Developer',

        company:
          'NovaSoft',

        location:
          'Lahore, Pakistan',

        description:
          `Backend development role using .NET,
PostgreSQL, REST APIs, Docker and Azure services.`,

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


      analysis: {

        jobId:
          'job-2',

        matchScore:
          74,

        recommendation:
          'POSSIBLE_MATCH',

        summary:
          `Your .NET, API and database experience matches
the core role, but Docker and Azure are notable skill gaps.`,

        matchedSkills: [

          'ASP.NET Core',

          'C#',

          'PostgreSQL',

          'REST APIs'

        ],

        missingSkills: [

          'Docker',

          'Azure'

        ],

        requirements: [

          {
            skill:
              'ASP.NET Core',

            required:
              true,

            matched:
              true
          },

          {
            skill:
              'PostgreSQL',

            required:
              true,

            matched:
              true
          },

          {
            skill:
              'Docker',

            required:
              true,

            matched:
              false
          },

          {
            skill:
              'Azure',

            required:
              true,

            matched:
              false
          }

        ],

        relevantExperience: [

          {
            id:
              'project-1',

            type:
              'PROJECT',

            title:
              'Full-Stack E-Commerce',

            content:
              `Used ASP.NET Core, PostgreSQL,
Entity Framework Core and REST APIs.`,

            similarityScore:
              0.84
          }

        ],

        analyzedAt:
          '2026-10-04T09:00:00Z'

      }

    }

  };


  constructor() {

    const id =
      this.route.snapshot
        .paramMap
        .get('id');


    if (!id) {

      this.notFound.set(
        true
      );

      this.loading.set(
        false
      );

      return;

    }


    const details =
      this.mockJobs[id];


    window.setTimeout(
      () => {

        if (!details) {

          this.notFound.set(
            true
          );

        } else {

          this.jobDetails.set(
            details
          );

        }


        this.loading.set(
          false
        );

      },
      250
    );

  }


  protected backToJobs(): void {

    this.router.navigate([
      '/jobs'
    ]);

  }


  protected generateOutreach(): void {

    const details =
      this.jobDetails();


    if (!details) {

      return;

    }


    this.router.navigate(
      [
        '/outreach'
      ],
      {
        queryParams: {
          jobId:
            details.job.id
        }
      }
    );

  }


  protected getRecommendationLabel(
    recommendation:
      MatchRecommendation
  ): string {

    switch (
      recommendation
    ) {

      case 'STRONG_MATCH':

        return 'Strong Match';


      case 'POSSIBLE_MATCH':

        return 'Possible Match';


      case 'LOW_MATCH':

        return 'Low Match';

    }

  }


  protected getRecommendationClass(
    recommendation:
      MatchRecommendation
  ): string {

    switch (
      recommendation
    ) {

      case 'STRONG_MATCH':

        return 'badge badge-success';


      case 'POSSIBLE_MATCH':

        return 'badge badge-warning';


      case 'LOW_MATCH':

        return 'badge badge-danger';

    }

  }

}