export type ApplicationStatus =
  | 'DRAFT'
  | 'READY'
  | 'SENT'
  | 'REPLIED'
  | 'INTERVIEW'
  | 'REJECTED'
  | 'OFFER';


export interface Application {

  id: string;

  jobId: string;

  jobTitle: string;

  company: string;

  location?: string;

  matchScore?: number;

  status: ApplicationStatus;

  contactName?: string;

  contactEmail?: string;

  outreachId?: string;

  appliedAt?: string;

  lastUpdatedAt: string;

  notes?: string;
}


export interface UpdateApplicationStatusRequest {

  status: ApplicationStatus;

  notes?: string;
}