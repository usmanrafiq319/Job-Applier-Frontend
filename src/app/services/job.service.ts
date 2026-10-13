import {inject,Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {API_ENDPOINTS} from '../core/constants/api-endpoints';
import {ApiClientService} from '../core/services/api-client.service';
import {AnalyzeJobRequest,CreateJobRequest,Job,JobStatus} from '../models/job.model';
import {JobAnalysisResponse} from '../models/job-analysis.model';


@Injectable({
  providedIn: 'root'
})
export class JobService {

  private readonly api =
    inject(ApiClientService);


  getJobs(): Observable<Job[]> {

    return this.api.get<Job[]>(
      API_ENDPOINTS.JOBS.LIST
    );
  }


  getJob(
    id: string
  ): Observable<Job> {

    return this.api.get<Job>(
      API_ENDPOINTS.JOBS.BY_ID(id)
    );
  }


  createJob(
    request: CreateJobRequest
  ): Observable<Job> {

    return this.api.post<
      Job,
      CreateJobRequest
    >(
      API_ENDPOINTS.JOBS.CREATE,
      request
    );
  }


  analyzeJob(
    request: AnalyzeJobRequest
  ): Observable<JobAnalysisResponse> {

    return this.api.post<
      JobAnalysisResponse,
      AnalyzeJobRequest
    >(
      API_ENDPOINTS.JOBS.ANALYZE,
      request
    );
  }


  updateStatus(
    jobId: string,
    status: JobStatus
  ): Observable<Job> {

    return this.api.patch<
      Job,
      { status: JobStatus }
    >(
      API_ENDPOINTS.JOBS.STATUS(jobId),
      {
        status
      }
    );
  }

}
