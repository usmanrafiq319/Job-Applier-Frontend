import {
  Job
} from './job.model';


export type MatchRecommendation =
  | 'STRONG_MATCH'
  | 'POSSIBLE_MATCH'
  | 'LOW_MATCH';


export type RequirementType =
  | 'SKILL'
  | 'EXPERIENCE'
  | 'EDUCATION'
  | 'RESPONSIBILITY'
  | 'OTHER';


export type RequirementImportance =
  | 'LOW'
  | 'MEDIUM'
  | 'HIGH';


export interface JobRequirement {

  id: string;

  text: string;

  requirementType: RequirementType;

  skillName?: string;

  required: boolean;

  importance: RequirementImportance;

  matched: boolean;
}


export interface RelevantExperience {

  id: string;

  type:
    | 'PROJECT'
    | 'EXPERIENCE'
    | 'RESUME';

  title: string;

  content: string;

  similarityScore: number;
}


export interface JobAnalysis {

  id: string;

  jobId: string;

  matchScore: number;

  recommendation:
    MatchRecommendation;

  summary: string;

  matchedSkills: string[];

  missingSkills: string[];

  requirements:
    JobRequirement[];

  relevantExperience:
    RelevantExperience[];

  analyzedAt: string;
}


export interface JobAnalysisResponse {

  job: Job;

  analysis: JobAnalysis;
}


export interface JobDetailsData {

  job: Job;

  analysis: JobAnalysis;
}