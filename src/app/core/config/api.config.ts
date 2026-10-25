// Loads environment/config values such as database URL, Groq key, Gemini key, model names, frontend URL, etc. It gives the rest of the application one centralized settings object instead of reading .env everywhere.

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