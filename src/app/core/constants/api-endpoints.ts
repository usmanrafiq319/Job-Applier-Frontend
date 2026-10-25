// Stores fixed application constants such as embedding dimension, resume chunk size, overlap size, and maximum upload size. These are values used in multiple files but which are not secrets or environment-specific settings.

export const API_ENDPOINTS = {

  DASHBOARD: {
    SUMMARY: '/dashboard'
  },

  PROFILE: {
    GET: '/profile',
    UPDATE: '/profile',

    SKILLS: '/profile/skills',
    PROJECTS: '/profile/projects',
    EXPERIENCES: '/profile/experiences',
    EDUCATION: '/profile/education'
  },

  RESUME: {
    UPLOAD: '/profile/resume',
    GET: '/profile/resume',
    DELETE: '/profile/resume',
    SEARCH: '/profile/resume/search'
  },

  JOBS: {
    LIST: '/jobs',

    CREATE: '/jobs',

    ANALYZE: '/jobs/analyze',

    BY_ID: (id: string) =>
      `/jobs/${id}`,

    STATUS: (id: string) =>
      `/jobs/${id}/status`
  },

  AGENT: {
    ANALYZE_JOB:
      '/agent/analyze-job'
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
  }

} as const;