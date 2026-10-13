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
  Application,
  UpdateApplicationStatusRequest
} from '../models/application.model';


@Injectable({
  providedIn: 'root'
})
export class ApplicationService {

  private readonly api =
    inject(ApiClientService);


  getApplications(): Observable<Application[]> {

    return this.api.get<Application[]>(
      API_ENDPOINTS.APPLICATIONS.LIST
    );
  }


  getApplication(
    id: string
  ): Observable<Application> {

    return this.api.get<Application>(
      API_ENDPOINTS.APPLICATIONS.BY_ID(id)
    );
  }


  updateStatus(
    id: string,
    request: UpdateApplicationStatusRequest
  ): Observable<Application> {

    return this.api.patch<
      Application,
      UpdateApplicationStatusRequest
    >(
      API_ENDPOINTS.APPLICATIONS.STATUS(id),
      request
    );
  }

}