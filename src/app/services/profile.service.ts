import { inject, Injectable } from '@angular/core';
import { ApiClientService } from '../core/services/api-client.service';
import { Observable } from 'rxjs';
import { UpdateProfileRequest, UserProfile } from '../models/profile.model';
import { API_ENDPOINTS } from '../core/constants/api-endpoints';

@Injectable({
  providedIn: 'root',
})
export class ProfileService {

  private readonly api =
    inject(ApiClientService);


  getProfile(): Observable<UserProfile> {

    return this.api.get<UserProfile>(
      API_ENDPOINTS.PROFILE.GET
    );
  }


  updateProfile(
    request: UpdateProfileRequest
  ): Observable<UserProfile> {

    return this.api.put<
      UserProfile,
      UpdateProfileRequest
    >(
      API_ENDPOINTS.PROFILE.UPDATE,
      request
    );
  }

}