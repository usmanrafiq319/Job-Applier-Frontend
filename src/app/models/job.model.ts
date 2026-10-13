export type JobStatus =
  | 'FOUND'
  | 'ANALYZED'
  | 'HIGH_MATCH'
  | 'LOW_MATCH'
  | 'SAVED'
  | 'REJECTED'
  | 'APPLIED';


export type EmploymentType =
  | 'FULL_TIME'
  | 'PART_TIME'
  | 'CONTRACT'
  | 'INTERNSHIP'
  | 'REMOTE'
  | 'OTHER';


export interface Job {

  id: string;

  title: string;

  company: string;

  location?: string;

  description: string;

  jobUrl?: string;

  employmentType?: EmploymentType;

  experienceRequired?: string;

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
}


export interface AnalyzeJobRequest {

  title: string;

  company: string;

  location?: string;

  description: string;

  jobUrl?: string;
}