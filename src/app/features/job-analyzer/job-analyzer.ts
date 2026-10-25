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
  Router
} from '@angular/router';

import {
  HttpErrorResponse
} from '@angular/common/http';

import {
  CreateJobRequest
} from '../../models/job.model';

import {
  JobAnalysisResponse,
  MatchRecommendation
} from '../../models/job-analysis.model';

import {
  JobService
} from '../../services/job.service';


@Component({
  selector: 'app-job-analyzer',

  imports: [
    ReactiveFormsModule
  ],

  templateUrl:
    './job-analyzer.html',

  styleUrl:
    './job-analyzer.css'
})
export class JobAnalyzer {

  private readonly fb =
    inject(FormBuilder);

  private readonly router =
    inject(Router);

  private readonly jobService =
    inject(JobService);


  protected readonly analyzing =
    signal(false);


  protected readonly analysis =
    signal<
      JobAnalysisResponse | null
    >(null);


  protected readonly analysisError =
    signal<string | null>(
      null
    );


  protected readonly form =
    this.fb.nonNullable.group({

      title: [
        '',
        Validators.required
      ],

      company: [
        '',
        Validators.required
      ],

      location: [
        'Lahore, Pakistan'
      ],

      jobUrl: [
        ''
      ],

      description: [
        '',
        [
          Validators.required,
          Validators.minLength(40)
        ]
      ]

    });


  protected analyzeJob(): void {

    if (this.form.invalid) {

      this.form.markAllAsTouched();

      return;

    }


    this.analyzing.set(
      true
    );

    this.analysis.set(
      null
    );

    this.analysisError.set(
      null
    );


    const formValue =
      this.form.getRawValue();


    const request:
      CreateJobRequest = {

      title:
        formValue.title,

      company:
        formValue.company,

      location:
        formValue.location,

      jobUrl:
        formValue.jobUrl,

      description:
        formValue.description,

      source:
        'MANUAL'

    };


    this.jobService
      .createAndAnalyzeJob(
        request
      )
      .subscribe({

        next: result => {

          this.analysis.set(
            result
          );

          this.analyzing.set(
            false
          );

        },


        error: (
          error: HttpErrorResponse
        ) => {

          console.error(
            'Job analysis failed:',
            error
          );


          const detail =
            error.error?.detail;


          this.analysisError.set(
            typeof detail === 'string'
              ? detail
              : 'Unable to analyze the job.'
          );


          this.analyzing.set(
            false
          );

        }

      });

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

        return (
          'badge badge-success'
        );


      case 'POSSIBLE_MATCH':

        return (
          'badge badge-warning'
        );


      case 'LOW_MATCH':

        return (
          'badge badge-danger'
        );

    }

  }


  protected reset(): void {

    this.form.reset({

      title: '',

      company: '',

      location:
        'Lahore, Pakistan',

      jobUrl: '',

      description: ''

    });


    this.analysis.set(
      null
    );


    this.analysisError.set(
      null
    );

  }


  protected viewJobs(): void {

    this.router.navigate([
      '/jobs'
    ]);

  }


  protected hasError(
    controlName:
      keyof typeof this.form.controls
  ): boolean {

    const control =
      this.form.controls[
        controlName
      ];


    return (
      control.invalid
      &&
      (
        control.touched
        ||
        control.dirty
      )
    );

  }

}