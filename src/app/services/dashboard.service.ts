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
  DashboardData
} from '../models/dashboard.model';


@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  private readonly api =
    inject(ApiClientService);


  getDashboard():
    Observable<DashboardData> {

    return this.api.get<DashboardData>(
      API_ENDPOINTS.DASHBOARD.SUMMARY
    );
  }

}