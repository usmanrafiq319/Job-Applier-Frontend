import {Component,signal} from '@angular/core';
import {DashboardData} from '../../models/dashboard.model';
import { StatCard } from '../../shared/components/stat-card/stat-card';
import { AgentActivity } from '../../shared/components/agent-activity/agent-activity';
import { AgentRun } from '../../models/agent.model';


@Component({
  selector: 'app-dashboard',

  imports: [StatCard,AgentActivity],

  templateUrl: './dashboard.html',

  styleUrl: './dashboard.css'
})
export class Dashboard {

  /*
   * Temporary frontend mock data.
   *
   * Later this will come from:
   *
   * DashboardService.getDashboard()
   *
   * GET /api/v1/dashboard
   */
  protected readonly dashboard =
    signal<DashboardData>({

      stats: {

        jobsFound: 24,

        jobsAnalyzed: 18,

        highMatches: 8,

        applicationsSent: 5,

        replies: 2,

        interviews: 1

      },

      recentJobs: [

        {
          id: '1',

          title: 'Junior .NET Developer',

          company: 'Tech Solutions',

          location: 'Lahore, Pakistan',

          description:
            'ASP.NET Core, Angular, SQL and REST API development.',

          status: 'HIGH_MATCH',

          matchScore: 88,

          createdAt:
            '2026-10-05T10:00:00Z'
        },

        {
          id: '2',

          title: 'Backend Developer',

          company: 'Software House',

          location: 'Lahore, Pakistan',

          description:
            '.NET backend role using PostgreSQL and APIs.',

          status: 'ANALYZED',

          matchScore: 76,

          createdAt:
            '2026-10-04T12:00:00Z'
        },

        {
          id: '3',

          title: 'AI Backend Intern',

          company: 'AI Labs',

          location: 'Remote',

          description:
            'FastAPI, LLMs, RAG and vector database work.',

          status: 'HIGH_MATCH',

          matchScore: 82,

          createdAt:
            '2026-10-03T09:00:00Z'
        }

      ],

      recentApplications: [

        {
          id: '1',

          jobId: '1',

          jobTitle:
            'Junior .NET Developer',

          company:
            'Tech Solutions',

          location:
            'Lahore, Pakistan',

          matchScore: 88,

          status: 'SENT',

          contactEmail:
            'careers@example.com',

          appliedAt:
            '2026-10-04T15:00:00Z',

          lastUpdatedAt:
            '2026-10-04T15:00:00Z'
        },

        {
          id: '2',

          jobId: '3',

          jobTitle:
            'AI Backend Intern',

          company:
            'AI Labs',

          location:
            'Remote',

          matchScore: 82,

          status: 'READY',

          contactEmail:
            'jobs@example.com',

          lastUpdatedAt:
            '2026-10-05T09:00:00Z'
        }

      ]

    });

protected readonly agentRun =
  signal<AgentRun>({

    id:
      'run-1',

    jobId:
      'job-1',

    status:
      'RUNNING',

    currentStep:
      'RETRIEVE_EXPERIENCE',

    progress:
      50,

    message:
      'Retrieving relevant project experience...',

    startedAt:
      new Date()
        .toISOString()

  });

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


  protected getApplicationBadgeClass(
    status: string
  ): string {

    switch (status) {

      case 'SENT':
      case 'REPLIED':
      case 'INTERVIEW':
      case 'OFFER':

        return 'badge badge-success';


      case 'READY':
      case 'DRAFT':

        return 'badge badge-warning';


      case 'REJECTED':

        return 'badge badge-danger';


      default:

        return 'badge badge-neutral';

    }

  }

}