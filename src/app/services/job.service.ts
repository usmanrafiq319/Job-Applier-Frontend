import {
  inject,
  Injectable
} from '@angular/core';

import {
  Observable,
  map,
  switchMap
} from 'rxjs';

import {
  API_ENDPOINTS
} from '../core/constants/api-endpoints';

import {
  ApiClientService
} from '../core/services/api-client.service';

import {
  AnalyzeJobRequest,
  CreateJobRequest,
  Job,
  JobStatus
} from '../models/job.model';

import {
  JobAnalysis,
  JobAnalysisResponse
} from '../models/job-analysis.model';


/*
 * These interfaces represent the
 * FastAPI JSON exactly.
 *
 * They intentionally use snake_case.
 */

interface JobApiResponse {

  id: string;

  title: string;

  company: string;

  location: string | null;

  job_url: string | null;

  description: string;

  status: JobStatus;

  source: string | null;

  created_at: string;

  updated_at: string;
}


interface JobRequirementApiResponse {

  id: string;

  text: string;

  requirement_type:
    | 'SKILL'
    | 'EXPERIENCE'
    | 'EDUCATION'
    | 'RESPONSIBILITY'
    | 'OTHER';

  skill_name: string | null;

  is_required: boolean;

  importance:
    | 'LOW'
    | 'MEDIUM'
    | 'HIGH';
}


interface RelevantEvidenceApiResponse {

  source:
    | 'project'
    | 'experience'
    | 'resume';

  source_id: string;

  title: string;

  content: string;

  relevance: number;
}


interface JobAnalysisApiResponse {

  id: string;

  job_id: string;

  match_score: number;

  recommendation:
    | 'STRONG_MATCH'
    | 'POSSIBLE_MATCH'
    | 'LOW_MATCH';

  matched_skills: string[];

  missing_skills: string[];

  relevant_experience:
    RelevantEvidenceApiResponse[];

  summary: string | null;

  analyzed_at: string;

  requirements:
    JobRequirementApiResponse[];
}


@Injectable({
  providedIn: 'root'
})
export class JobService {

  private readonly api =
    inject(ApiClientService);


  getJobs():
    Observable<Job[]> {

    return this.api
      .get<JobApiResponse[]>(
        API_ENDPOINTS.JOBS.LIST
      )
      .pipe(
        map(
          jobs =>
            jobs.map(
              job =>
                this.mapJob(job)
            )
        )
      );
  }


  getJob(
    id: string
  ): Observable<Job> {

    return this.api
      .get<JobApiResponse>(
        API_ENDPOINTS.JOBS.BY_ID(id)
      )
      .pipe(
        map(
          job =>
            this.mapJob(job)
        )
      );
  }


  createJob(
    request: CreateJobRequest
  ): Observable<Job> {

    const body = {

      title:
        request.title,

      company:
        request.company,

      location:
        request.location || null,

      description:
        request.description,

      job_url:
        request.jobUrl || null,

      source:
        request.source || null

    };


    return this.api
      .post<
        JobApiResponse,
        typeof body
      >(
        API_ENDPOINTS.JOBS.CREATE,
        body
      )
      .pipe(
        map(
          job =>
            this.mapJob(job)
        )
      );
  }


  analyzeJob(
    request: AnalyzeJobRequest
  ): Observable<JobAnalysis> {

    const body = {

      job_id:
        request.jobId,

      resume_limit:
        request.resumeLimit ?? 5

    };


    return this.api
      .post<
        JobAnalysisApiResponse,
        typeof body
      >(
        API_ENDPOINTS.JOBS.ANALYZE,
        body
      )
      .pipe(
        map(
          analysis =>
            this.mapAnalysis(
              analysis
            )
        )
      );
  }


  /*
   * This method matches the current
   * Job Analyzer screen.
   *
   * Form data
   *    ↓
   * create job
   *    ↓
   * get job UUID
   *    ↓
   * analyze job
   *    ↓
   * return UI-ready result
   */
  createAndAnalyzeJob(
    request: CreateJobRequest
  ): Observable<JobAnalysisResponse> {

    return this.createJob(
      request
    )
      .pipe(

        switchMap(
          job =>

            this.analyzeJob({
              jobId:
                job.id,

              resumeLimit:
                5
            })
              .pipe(

                map(
                  analysis => ({
                    job,
                    analysis
                  })
                )

              )

        )

      );
  }


  updateStatus(
    jobId: string,
    status: JobStatus
  ): Observable<Job> {

    return this.api
      .patch<
        JobApiResponse,
        { status: JobStatus }
      >(
        API_ENDPOINTS.JOBS
          .STATUS(jobId),

        {
          status
        }
      )
      .pipe(
        map(
          job =>
            this.mapJob(job)
        )
      );
  }


  private mapJob(
    job: JobApiResponse
  ): Job {

    return {

      id:
        job.id,

      title:
        job.title,

      company:
        job.company,

      location:
        job.location ?? undefined,

      description:
        job.description,

      jobUrl:
        job.job_url ?? undefined,

      source:
        job.source ?? undefined,

      status:
        job.status,

      createdAt:
        job.created_at,

      updatedAt:
        job.updated_at

    };
  }


  private mapAnalysis(
    analysis: JobAnalysisApiResponse
  ): JobAnalysis {

    const matchedSkills =
      new Set(
        analysis.matched_skills
          .map(
            skill =>
              skill.toLowerCase()
          )
      );


    return {

      id:
        analysis.id,

      jobId:
        analysis.job_id,

      matchScore:
        analysis.match_score,

      recommendation:
        analysis.recommendation,

      summary:
        analysis.summary ?? '',

      matchedSkills:
        analysis.matched_skills,

      missingSkills:
        analysis.missing_skills,

      analyzedAt:
        analysis.analyzed_at,


      requirements:
        analysis.requirements.map(
          requirement => ({

            id:
              requirement.id,

            text:
              requirement.text,

            requirementType:
              requirement
                .requirement_type,

            skillName:
              requirement.skill_name
                ?? undefined,

            required:
              requirement.is_required,

            importance:
              requirement.importance,

            matched:
              requirement.skill_name
                ? matchedSkills.has(
                    requirement
                      .skill_name
                      .toLowerCase()
                  )
                : false

          })
        ),


      relevantExperience:
        analysis
          .relevant_experience
          .map(
            evidence => ({

              id:evidence.source_id,

              type:evidence.source.toUpperCase()  as |'PROJECT'| 'EXPERIENCE'|'RESUME' ,

              title:evidence.title,

              content:
                evidence.content,

              similarityScore:
                evidence.relevance

            })
          )

    };
  }

}