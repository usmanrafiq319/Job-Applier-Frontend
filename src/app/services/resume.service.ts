import {inject,Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {API_ENDPOINTS} from '../core/constants/api-endpoints';
import {ApiClientService} from '../core/services/api-client.service';
import {Resume,ResumeUploadResponse} from '../models/resume.model';


@Injectable({
  providedIn: 'root'
})
export class ResumeService {

  private readonly api =
    inject(ApiClientService);


  getResume(): Observable<Resume> {

    return this.api.get<Resume>(
      API_ENDPOINTS.RESUME.GET
    );
  }


  uploadResume(
    file: File
  ): Observable<ResumeUploadResponse> {

    return this.api.upload<ResumeUploadResponse>(
      API_ENDPOINTS.RESUME.UPLOAD,
      file
    );
  }


  deleteResume(): Observable<void> {

    return this.api.delete<void>(
      API_ENDPOINTS.RESUME.DELETE
    );
  }

}
