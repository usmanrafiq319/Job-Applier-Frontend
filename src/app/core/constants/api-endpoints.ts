export const API_ENDPOINTS = {

  DASHBOARD: {
    SUMMARY: '/dashboard'
  },

  PROFILE: {
    GET: '/profile',
    UPDATE: '/profile'
  },

  RESUME: {
    UPLOAD: '/profile/resume',
    GET: '/profile/resume',
    DELETE: '/profile/resume'
  },

  JOBS: {
    LIST: '/jobs',
    CREATE: '/jobs',
    ANALYZE: '/jobs/analyze',

    BY_ID: (id: string) => `/jobs/${id}`,

    STATUS: (id: string) =>
      `/jobs/${id}/status`
  },

  OUTREACH: {
    GENERATE: '/outreach/generate',

    BY_ID: (id: string) =>
      `/outreach/${id}`,

    APPROVE: (id: string) =>
      `/outreach/${id}/approve`,

    GMAIL_DRAFT: (id: string) =>
      `/outreach/${id}/gmail-draft`
  },

  APPLICATIONS: {
    LIST: '/applications',

    BY_ID: (id: string) =>
      `/applications/${id}`,

    STATUS: (id: string) =>
      `/applications/${id}/status`
  },

  AGENT: {
    RUNS: '/agent/runs',

    RUN_BY_ID: (id: string) =>
      `/agent/runs/${id}`
  }

} as const;