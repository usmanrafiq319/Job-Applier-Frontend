export type AgentRunStatus =
  | 'PENDING'
  | 'RUNNING'
  | 'WAITING_FOR_APPROVAL'
  | 'COMPLETED'
  | 'FAILED'
  | 'CANCELLED';


export type AgentStep =
  | 'LOAD_PROFILE'
  | 'PARSE_JOB'
  | 'ANALYZE_REQUIREMENTS'
  | 'MATCH_PROFILE'
  | 'RETRIEVE_EXPERIENCE'
  | 'CALCULATE_SCORE'
  | 'GENERATE_EMAIL'
  | 'WAIT_FOR_APPROVAL'
  | 'CREATE_GMAIL_DRAFT'
  | 'SAVE_APPLICATION';


export interface AgentRun {

  id: string;

  jobId?: string;

  status: AgentRunStatus;

  currentStep?: AgentStep;

  progress?: number;

  message?: string;

  startedAt?: string;

  finishedAt?: string;

  error?: string;
}