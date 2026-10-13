import { Application } from './application.model';
import { Job } from './job.model';


export interface DashboardStats {

  jobsFound: number;

  jobsAnalyzed: number;

  highMatches: number;

  applicationsSent: number;

  replies: number;

  interviews: number;
}


export interface DashboardData {

  stats: DashboardStats;

  recentJobs: Job[];

  recentApplications: Application[];
}