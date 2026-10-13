import { InjectionToken } from '@angular/core';

export interface ApiConfig {
  baseUrl: string;
  apiVersion: string;
}

export const API_CONFIG = new InjectionToken<ApiConfig>('API_CONFIG');

export const apiConfig: ApiConfig = {

  baseUrl:
    'http://127.0.0.1:8000',

  apiVersion:
    'v1'

};