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
  AnalyzeJobRequest
} from '../../models/job.model';

import {
  JobAnalysisResponse,
  MatchRecommendation
} from '../../models/job-analysis.model';


@Component({
  selector: 'app-job-analyzer',

  imports: [
    ReactiveFormsModule
  ],

  templateUrl: './job-analyzer.html',

  styleUrl: './job-analyzer.css'
})
export class JobAnalyzer {

  private readonly fb =
    inject(FormBuilder);

  private readonly router =
    inject(Router);


  /*
   * Later:
   *
   * private readonly jobService =
   *   inject(JobService);
   *
   * this.jobService
   *   .analyzeJob(request)
   *   .subscribe(...)
   */


  protected readonly analyzing =
    signal(false);


  protected readonly analysis =
    signal<JobAnalysisResponse | null>(
      null
    );


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


  /*
   * Temporary frontend knowledge.
   *
   * This will disappear once FastAPI +
   * LangGraph perform the real analysis.
   */
  private readonly profileSkills =
    new Set([

      'ASP.NET Core',

      'C#',

      'Angular',

      'SQL',

      'PostgreSQL',

      'REST APIs',

      'Entity Framework Core',

      'SignalR',

      'FastAPI',

      'LangChain',

      'LangGraph',

      'RAG',

      'Tailwind CSS'

    ]);


  /*
   * Only for frontend simulation.
   *
   * This lets you paste different job
   * descriptions and still see different
   * mock results.
   */
  private readonly knownSkills = [

    {
      name: 'ASP.NET Core',
      keywords: [
        'asp.net',
        'asp.net core',
        '.net core'
      ]
    },

    {
      name: 'C#',
      keywords: [
        'c#',
        'c sharp'
      ]
    },

    {
      name: 'Angular',
      keywords: [
        'angular'
      ]
    },

    {
      name: 'SQL',
      keywords: [
        'sql'
      ]
    },

    {
      name: 'PostgreSQL',
      keywords: [
        'postgresql',
        'postgres'
      ]
    },

    {
      name: 'REST APIs',
      keywords: [
        'rest',
        'rest api',
        'restful'
      ]
    },

    {
      name: 'Entity Framework Core',
      keywords: [
        'entity framework',
        'ef core'
      ]
    },

    {
      name: 'SignalR',
      keywords: [
        'signalr'
      ]
    },

    {
      name: 'FastAPI',
      keywords: [
        'fastapi'
      ]
    },

    {
      name: 'LangChain',
      keywords: [
        'langchain'
      ]
    },

    {
      name: 'LangGraph',
      keywords: [
        'langgraph'
      ]
    },

    {
      name: 'RAG',
      keywords: [
        'rag',
        'retrieval augmented'
      ]
    },

    {
      name: 'Docker',
      keywords: [
        'docker'
      ]
    },

    {
      name: 'Azure',
      keywords: [
        'azure'
      ]
    },

    {
      name: 'AWS',
      keywords: [
        'aws',
        'amazon web services'
      ]
    }

  ];


  protected analyzeJob(): void {

    if (this.form.invalid) {

      this.form.markAllAsTouched();

      return;

    }


    this.analyzing.set(true);

    this.analysis.set(null);

    this.analysisError.set(null);


    const request:
      AnalyzeJobRequest =
      this.form.getRawValue();


    /*
     * Temporary delay to simulate
     * backend / LangGraph execution.
     */
    window.setTimeout(
      () => {

        try {

          const result =
            this.buildMockAnalysis(
              request
            );


          this.analysis.set(
            result
          );

        }
        catch {

          this.analysisError.set(
            'Unable to analyze the job.'
          );

        }
        finally {

          this.analyzing.set(
            false
          );

        }

      },
      700
    );

  }


  private buildMockAnalysis(
    request: AnalyzeJobRequest
  ): JobAnalysisResponse {

    const description =
      request.description
        .toLowerCase();


    const requirements =
      this.knownSkills
        .filter(
          skill =>
            skill.keywords.some(
              keyword =>
                description.includes(
                  keyword
                )
            )
        );


    /*
     * If user pasted a generic job
     * with no known keywords,
     * provide a small sample.
     */
    const detectedRequirements =
      requirements.length > 0
        ? requirements
        : [
            {
              name: 'ASP.NET Core',
              keywords: []
            },

            {
              name: 'Angular',
              keywords: []
            },

            {
              name: 'Azure',
              keywords: []
            }
          ];


    const matchedSkills =
      detectedRequirements
        .filter(
          requirement =>
            this.profileSkills.has(
              requirement.name
            )
        )
        .map(
          requirement =>
            requirement.name
        );


    const missingSkills =
      detectedRequirements
        .filter(
          requirement =>
            !this.profileSkills.has(
              requirement.name
            )
        )
        .map(
          requirement =>
            requirement.name
        );


    const total =
      detectedRequirements.length;


    const ratio =
      total === 0
        ? 0
        : matchedSkills.length / total;


    const matchScore =
      Math.min(
        95,
        Math.max(
          30,
          Math.round(
            30 + ratio * 65
          )
        )
      );


    const recommendation:
      MatchRecommendation =
      matchScore >= 80
        ? 'STRONG_MATCH'
        : matchScore >= 60
          ? 'POSSIBLE_MATCH'
          : 'LOW_MATCH';


    return {

      job: {

        id:
          `job-${Date.now()}`,

        title:
          request.title,

        company:
          request.company,

        location:
          request.location

      },


      analysis: {

        jobId:
          `job-${Date.now()}`,

        matchScore,

        recommendation,

        summary:
          this.createSummary(
            matchScore,
            matchedSkills,
            missingSkills
          ),

        matchedSkills,

        missingSkills,

        requirements:
          detectedRequirements.map(
            requirement => ({

              skill:
                requirement.name,

              required:
                true,

              matched:
                this.profileSkills.has(
                  requirement.name
                )

            })
          ),

        relevantExperience: [

          {
            id: 'experience-1',

            type: 'EXPERIENCE',

            title:
              '.NET Full-Stack Internship',

            content:
              'Worked with ASP.NET Core, Angular, REST APIs, SQL and real-time application features.',

            similarityScore:
              0.89
          },

          {
            id: 'project-1',

            type: 'PROJECT',

            title:
              'Full-Stack E-Commerce',

            content:
              'Built an ASP.NET Core and Angular application with JWT, PostgreSQL, SignalR and Cloudflare R2.',

            similarityScore:
              0.86
          },

          {
            id: 'project-2',

            type: 'PROJECT',

            title:
              'AI Knowledge Hub',

            content:
              'Built a FastAPI RAG backend using PostgreSQL, pgvector, Gemini and Groq.',

            similarityScore:
              0.76
          }

        ],

        analyzedAt:
          new Date()
            .toISOString()

      }

    };

  }


  private createSummary(
    score: number,
    matched: string[],
    missing: string[]
  ): string {

    if (score >= 80) {

      return `This looks like a strong opportunity. Your profile matches ${matched.length} important requirements, with only a few potential gaps.`;

    }


    if (score >= 60) {

      return `This role has reasonable alignment with your current experience, but you should review the missing skills before applying.`;

    }


    return `This role currently has a lower match with your profile. Review the missing requirements before deciding whether to apply.`;

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
      control.invalid &&
      (
        control.touched ||
        control.dirty
      )
    );

  }

}