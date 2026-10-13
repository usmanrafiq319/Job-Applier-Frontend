import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { API_CONFIG, ApiConfig } from '../config/api.config';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})

@Injectable({
  providedIn: 'root'
})
export class ApiClientService {

  private readonly http = inject(HttpClient);

  private readonly config =
    inject<ApiConfig>(API_CONFIG);


  private get baseUrl(): string {

    const baseUrl =
      this.config.baseUrl.replace(/\/+$/, '');

    const version =
      this.config.apiVersion.replace(/^\/+|\/+$/g, '');

    return `${baseUrl}/api/${version}`;
  }

  get<T>(
    endpoint: string,
    params?: HttpParams
  ): Observable<T> {

    return this.http.get<T>(
      `${this.baseUrl}${endpoint}`,
      {
        params
      }
    );
  }


  post<TResponse, TBody = unknown>(
    endpoint: string,
    body?: TBody
  ): Observable<TResponse> {

    return this.http.post<TResponse>(
      `${this.baseUrl}${endpoint}`,
      body
    );
  }


  put<TResponse, TBody = unknown>(
    endpoint: string,
    body: TBody
  ): Observable<TResponse> {

    return this.http.put<TResponse>(
      `${this.baseUrl}${endpoint}`,
      body
    );
  }


  patch<TResponse, TBody = unknown>(
    endpoint: string,
    body: TBody
  ): Observable<TResponse> {

    return this.http.patch<TResponse>(
      `${this.baseUrl}${endpoint}`,
      body
    );
  }


  delete<T>(
    endpoint: string
  ): Observable<T> {

    return this.http.delete<T>(
      `${this.baseUrl}${endpoint}`
    );
  }


  upload<T>(
    endpoint: string,
    file: File,
    fieldName = 'file'
  ): Observable<T> {

    const formData = new FormData();

    formData.append(
      fieldName,
      file
    );

    return this.http.post<T>(
      `${this.baseUrl}${endpoint}`,
      formData
    );
  }

}
