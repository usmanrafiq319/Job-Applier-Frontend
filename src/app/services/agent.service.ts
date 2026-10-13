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
  AgentRun
} from '../models/agent.model';


@Injectable({
  providedIn: 'root'
})
export class AgentService {

  private readonly api = inject(ApiClientService);


  getRuns(): Observable<AgentRun[]> {

    return this.api.get<AgentRun[]>(
      API_ENDPOINTS.AGENT.RUNS
    );
  }


  getRun(
    id: string
  ): Observable<AgentRun> {

    return this.api.get<AgentRun>(
      API_ENDPOINTS.AGENT.RUN_BY_ID(id)
    );
  }

}