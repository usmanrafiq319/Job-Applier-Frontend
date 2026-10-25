export type JobStatus =
  | 'FOUND'
  | 'ANALYZED'
  | 'HIGH_MATCH'
  | 'LOW_MATCH'
  | 'SAVED'
  | 'REJECTED'
  | 'APPLIED';


export interface Job {

  id: string;

  title: string;

  company: string;

  location?: string;

  description: string;

  jobUrl?: string;

  source?: string;

  status: JobStatus;

  matchScore?: number;

  createdAt: string;

  updatedAt?: string;
}


export interface CreateJobRequest {

  title: string;

  company: string;

  location?: string;

  description: string;

  jobUrl?: string;

  source?: string;
}


export interface AnalyzeJobRequest {

  jobId: string;

  resumeLimit?: number;
}