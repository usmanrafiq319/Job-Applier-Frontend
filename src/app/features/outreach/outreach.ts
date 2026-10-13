import {
  Component,
  inject,
  signal
} from '@angular/core';

import {
  FormBuilder,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';

import {
  ActivatedRoute,
  Router
} from '@angular/router';

import {
  EmailDraft,
  EmailDraftStatus
} from '../../models/outreach.model';


interface OutreachJobContext {

  id: string;

  title: string;

  company: string;

  location?: string;

  matchScore: number;

}


@Component({
  selector: 'app-outreach',

  imports: [
    ReactiveFormsModule
  ],

  templateUrl: './outreach.html',

  styleUrl: './outreach.css'
})
export class Outreach {

  private readonly fb =
    inject(FormBuilder);

  private readonly route =
    inject(ActivatedRoute);

  private readonly router =
    inject(Router);


  protected readonly generating =
    signal(false);


  protected readonly draft =
    signal<EmailDraft | null>(
      null
    );


  protected readonly currentStatus =
    signal<EmailDraftStatus | null>(
      null
    );


  protected readonly message =
    signal<string | null>(
      null
    );


  /*
   * Temporary selected job.
   *
   * Later:
   *
   * JobService.getJob(jobId)
   */
  protected readonly job =
    signal<OutreachJobContext | null>(
      null
    );


  protected readonly contactForm =
    this.fb.nonNullable.group({

      recipientName: [
        'Hiring Team'
      ],

      recipientEmail: [
        '',
        [
          Validators.email
        ]
      ]

    });


  protected readonly emailForm =
    this.fb.nonNullable.group({

      subject: [
        '',
        Validators.required
      ],

      body: [
        '',
        [
          Validators.required,
          Validators.minLength(40)
        ]
      ]

    });


  private readonly mockJobs:
    Record<string, OutreachJobContext> = {

    'job-1': {

      id:
        'job-1',

      title:
        'Junior .NET Developer',

      company:
        'Tech Solutions',

      location:
        'Lahore, Pakistan',

      matchScore:
        88

    },


    'job-2': {

      id:
        'job-2',

      title:
        '.NET Backend Developer',

      company:
        'NovaSoft',

      location:
        'Lahore, Pakistan',

      matchScore:
        74

    },


    'job-3': {

      id:
        'job-3',

      title:
        'AI Backend Intern',

      company:
        'AI Labs',

      location:
        'Remote, Pakistan',

      matchScore:
        82

    }

  };


  constructor() {

    const jobId =
      this.route.snapshot
        .queryParamMap
        .get('jobId');


    if (
      jobId &&
      this.mockJobs[jobId]
    ) {

      this.job.set(
        this.mockJobs[jobId]
      );

    } else {

      this.job.set(
        this.mockJobs['job-1']
      );

    }

  }


  protected generateEmail(): void {

    const selectedJob =
      this.job();


    if (!selectedJob) {

      return;

    }


    this.generating.set(
      true
    );


    this.message.set(
      null
    );


    /*
     * Later:
     *
     * this.outreachService
     *   .generateEmail({
     *      jobId,
     *      recipientName,
     *      recipientEmail
     *   })
     */


    window.setTimeout(
      () => {

        const recipientName =
          this.contactForm.controls
            .recipientName.value;


        const subject =
          `Application for ${selectedJob.title}`;


        const greeting =
          recipientName
            ? `Hi ${recipientName},`
            : 'Hello Hiring Team,';


        const body =
`${greeting}

I came across the ${selectedJob.title} opportunity at ${selectedJob.company} and was interested because the role strongly aligns with my current .NET full-stack experience.

I recently completed a .NET Full-Stack internship where I worked with ASP.NET Core, Angular, REST APIs, SQL databases and real-time application features.

I also built a full-stack e-commerce application using ASP.NET Core, Angular, Entity Framework Core, PostgreSQL, JWT authentication, SignalR and Cloudflare R2.

Based on the role requirements, I believe my current experience provides a strong foundation for contributing to your team while continuing to grow as a developer.

I have attached my resume for your consideration and would be glad to discuss the opportunity further.

Best regards,
Rameel Hassan`;


        const draft:
          EmailDraft = {

          id:
            `draft-${Date.now()}`,

          jobId:
            selectedJob.id,

          recipientName:
            this.contactForm.controls
              .recipientName.value,

          recipientEmail:
            this.contactForm.controls
              .recipientEmail.value,

          subject,

          body,

          status:
            'GENERATED',

          createdAt:
            new Date()
              .toISOString()

        };


        this.draft.set(
          draft
        );


        this.currentStatus.set(
          'GENERATED'
        );


        this.emailForm.setValue({

          subject,

          body

        });


        this.generating.set(
          false
        );

      },
      650
    );

  }


  protected markEdited(): void {

    if (
      this.currentStatus() ===
      'GENERATED'
    ) {

      this.currentStatus.set(
        'EDITED'
      );

    }

  }


  protected approve(): void {

    if (
      this.emailForm.invalid
    ) {

      this.emailForm
        .markAllAsTouched();

      return;

    }


    const current =
      this.draft();


    if (!current) {

      return;

    }


    const updated:
      EmailDraft = {

      ...current,

      subject:
        this.emailForm.controls
          .subject.value,

      body:
        this.emailForm.controls
          .body.value,

      recipientName:
        this.contactForm.controls
          .recipientName.value,

      recipientEmail:
        this.contactForm.controls
          .recipientEmail.value,

      status:
        'APPROVED',

      updatedAt:
        new Date()
          .toISOString()

    };


    this.draft.set(
      updated
    );


    this.currentStatus.set(
      'APPROVED'
    );


    this.message.set(
      'Email approved. It is ready to create as a Gmail draft.'
    );

  }


  protected createGmailDraft(): void {

    const current =
      this.draft();


    if (
      !current ||
      this.currentStatus() !==
      'APPROVED'
    ) {

      return;

    }


    /*
     * Later:
     *
     * this.outreachService
     *   .createGmailDraft(current.id)
     */


    const updated:
      EmailDraft = {

      ...current,

      status:
        'CREATED_IN_GMAIL',

      updatedAt:
        new Date()
          .toISOString()

    };


    this.draft.set(
      updated
    );


    this.currentStatus.set(
      'CREATED_IN_GMAIL'
    );


    this.message.set(
      'Mock Gmail draft created successfully.'
    );

  }


  protected backToJob(): void {

    const selectedJob =
      this.job();


    if (!selectedJob) {

      this.router.navigate([
        '/jobs'
      ]);

      return;

    }


    this.router.navigate([
      '/jobs',
      selectedJob.id
    ]);

  }


  protected getStatusClass():
    string {

    switch (
      this.currentStatus()
    ) {

      case 'GENERATED':

        return 'badge badge-info';


      case 'EDITED':

        return 'badge badge-warning';


      case 'APPROVED':

        return 'badge badge-success';


      case 'CREATED_IN_GMAIL':

        return 'badge badge-success';


      default:

        return 'badge badge-neutral';

    }

  }

}