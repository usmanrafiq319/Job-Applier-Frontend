import {
  inject,
  Injectable
} from '@angular/core';

import {
  Observable
} from 'rxjs';

import {
  API_ENDPOINTS
} from '../core/constants/api-endpoints';

import {
  ApiClientService
} from '../core/services/api-client.service';

import {
  ApproveEmailResponse,
  EmailDraft,
  GenerateEmailRequest,
  GmailDraftResponse,
  UpdateEmailDraftRequest
} from '../models/outreach.model';


@Injectable({
  providedIn: 'root'
})
export class OutreachService {

  private readonly api =
    inject(ApiClientService);


  generateEmail(
    request: GenerateEmailRequest
  ): Observable<EmailDraft> {

    return this.api.post<
      EmailDraft,
      GenerateEmailRequest
    >(
      API_ENDPOINTS.OUTREACH.GENERATE,
      request
    );
  }


  getDraft(
    id: string
  ): Observable<EmailDraft> {

    return this.api.get<EmailDraft>(
      API_ENDPOINTS.OUTREACH.BY_ID(id)
    );
  }


  updateDraft(
    id: string,
    request: UpdateEmailDraftRequest
  ): Observable<EmailDraft> {

    return this.api.put<
      EmailDraft,
      UpdateEmailDraftRequest
    >(
      API_ENDPOINTS.OUTREACH.BY_ID(id),
      request
    );
  }


  approveDraft(
    id: string
  ): Observable<ApproveEmailResponse> {

    return this.api.post<
      ApproveEmailResponse
    >(
      API_ENDPOINTS.OUTREACH.APPROVE(id)
    );
  }


  createGmailDraft(
    id: string
  ): Observable<GmailDraftResponse> {

    return this.api.post<
      GmailDraftResponse
    >(
      API_ENDPOINTS.OUTREACH.GMAIL_DRAFT(id)
    );
  }

}