import {Component,inject,signal} from '@angular/core';
import {FormBuilder,ReactiveFormsModule,Validators} from '@angular/forms';
import {Experience,Project,Skill} from '../../models/profile.model';

@Component({
  selector: 'app-profile',

  imports: [
    ReactiveFormsModule
  ],

  templateUrl: './profile.html',

  styleUrl: './profile.css'
})
export class Profile {

  private readonly fb = inject(FormBuilder);


  /*
   * Later:
   *
   * ProfileService.getProfile()
   * ProfileService.updateProfile()
   * ResumeService.uploadResume()
   */


  protected readonly profileForm =
    this.fb.nonNullable.group({

      fullName: [
        'Rameel Hassan',
        [
          Validators.required,
          Validators.minLength(3)
        ]
      ],

      email: [
        'rameel@example.com',
        [
          Validators.required,
          Validators.email
        ]
      ],

      phone: [
        ''
      ],

      location: [
        'Lahore, Pakistan'
      ],

      headline: [
        '.NET Full-Stack Developer | ASP.NET Core | Angular | AI & RAG'
      ],

      professionalSummary: [
        `Backend-focused developer with experience in ASP.NET Core,
Angular, REST APIs, PostgreSQL, FastAPI, RAG and AI integrations.`
      ],

      linkedinUrl: [
        ''
      ],

      githubUrl: [
        ''
      ],

      portfolioUrl: [
        'https://figma-ecom-mu.vercel.app/'
      ]

    });


  protected readonly skills =
    signal<Skill[]>([

      {
        name: 'ASP.NET Core',
        level: 'INTERMEDIATE',
        category: 'BACKEND'
      },

      {
        name: 'C#',
        level: 'INTERMEDIATE',
        category: 'BACKEND'
      },

      {
        name: 'Angular',
        level: 'INTERMEDIATE',
        category: 'FRONTEND'
      },

      {
        name: 'Tailwind CSS',
        level: 'INTERMEDIATE',
        category: 'FRONTEND'
      },

      {
        name: 'FastAPI',
        level: 'INTERMEDIATE',
        category: 'BACKEND'
      },

      {
        name: 'PostgreSQL',
        level: 'INTERMEDIATE',
        category: 'DATABASE'
      },

      {
        name: 'LangChain',
        level: 'BEGINNER',
        category: 'AI'
      },

      {
        name: 'LangGraph',
        level: 'BEGINNER',
        category: 'AI'
      },

      {
        name: 'RAG',
        level: 'BEGINNER',
        category: 'AI'
      },

      {
        name: 'pgvector',
        level: 'BEGINNER',
        category: 'AI'
      }

    ]);


  protected readonly projects =
    signal<Project[]>([

      {
        id: 'project-1',

        title:
          'Full-Stack E-Commerce',

        description:
          `Full-stack e-commerce platform with JWT authentication,
SignalR real-time chat, Cloudflare R2 storage and AI support.`,

        technologies: [
          'ASP.NET Core',
          'Angular',
          'Entity Framework Core',
          'PostgreSQL',
          'SignalR',
          'Cloudflare R2'
        ],

        projectUrl:
          'https://figma-ecom-mu.vercel.app/'
      },

      {
        id: 'project-2',

        title:
          'AI Knowledge Hub',

        description:
          `RAG backend using FastAPI, PostgreSQL, pgvector,
hybrid retrieval and LLM-powered answers.`,

        technologies: [
          'FastAPI',
          'PostgreSQL',
          'pgvector',
          'Gemini',
          'Groq',
          'RAG'
        ]
      }

    ]);


  protected readonly experience =
    signal<Experience[]>([

      {
        id: 'experience-1',

        company:
          'Glosix',

        role:
          '.NET Full-Stack Intern',

        startDate:
          '2026-02-01',

        endDate:
          '2026-08-31',

        currentlyWorking:
          false,

        description:
          `Worked with ASP.NET Core, Angular, REST APIs,
databases, authentication and real-time application features.`,

        technologies: [
          'ASP.NET Core',
          'Angular',
          'SQL',
          'REST APIs',
          'SignalR'
        ]
      }

    ]);


  protected readonly resumeFileName =
    signal<string | null>(
      'Rameel_Hassan_Resume.pdf'
    );


  protected readonly resumeStatus =
    signal<
      'READY' |
      'SELECTED' |
      'NONE'
    >('READY');


  protected readonly newSkill =
    signal('');


  protected readonly saved =
    signal(false);


  protected saveProfile(): void {

    if (this.profileForm.invalid) {

      this.profileForm.markAllAsTouched();

      return;

    }


    /*
     * Later:
     *
     * const request =
     *   this.profileForm.getRawValue();
     *
     * this.profileService
     *   .updateProfile(...)
     */


    console.log(
      'Profile:',
      this.profileForm.getRawValue()
    );

    console.log(
      'Skills:',
      this.skills()
    );


    this.saved.set(true);


    window.setTimeout(
      () => this.saved.set(false),
      2500
    );

  }


  protected selectResume(
    event: Event
  ): void {

    const input =
      event.target as HTMLInputElement;


    const file =
      input.files?.[0];


    if (!file) {

      return;

    }


    if (
      file.type !==
      'application/pdf'
    ) {

      input.value = '';

      return;

    }


    this.resumeFileName.set(
      file.name
    );


    this.resumeStatus.set(
      'SELECTED'
    );


    /*
     * Later:
     *
     * this.resumeService
     *   .uploadResume(file)
     */


  }


  protected addSkill(
    input: HTMLInputElement
  ): void {

    const value =
      input.value.trim();


    if (!value) {

      return;

    }


    const alreadyExists =
      this.skills()
        .some(
          skill =>
            skill.name
              .toLowerCase() ===
            value.toLowerCase()
        );


    if (alreadyExists) {

      input.value = '';

      return;

    }


    this.skills.update(
      current => [

        ...current,

        {
          name: value,
          level: 'BEGINNER',
          category: 'OTHER'
        }

      ]
    );


    input.value = '';

  }


  protected removeSkill(
    skillName: string
  ): void {

    this.skills.update(
      current =>
        current.filter(
          skill =>
            skill.name !==
            skillName
        )
    );

  }


  protected hasError(
    controlName:
      keyof typeof this.profileForm.controls
  ): boolean {

    const control =
      this.profileForm.controls[
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