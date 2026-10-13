import { Job } from './job.model';

export type MatchRecommendation =
  | 'STRONG_MATCH'
  | 'POSSIBLE_MATCH'
  | 'LOW_MATCH';


export interface JobRequirement {

  skill: string;

  required: boolean;

  matched: boolean;
}


export interface RelevantExperience {

  id?: string;

  type:
    | 'PROJECT'
    | 'EXPERIENCE'
    | 'SKILL'
    | 'RESUME';

  title: string;

  content: string;

  similarityScore?: number;
}


export interface JobAnalysis {

  jobId: string;

  matchScore: number;

  recommendation: MatchRecommendation;

  summary: string;

  matchedSkills: string[];

  missingSkills: string[];

  requirements: JobRequirement[];

  relevantExperience: RelevantExperience[];

  analyzedAt: string;
}


export interface JobAnalysisResponse {

  job: {
    id: string;

    title: string;

    company: string;

    location?: string;
  };

  analysis: JobAnalysis;
}

export interface JobDetailsData {
  job: Job;
  analysis: JobAnalysis;
}