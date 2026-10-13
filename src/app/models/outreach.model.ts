export type EmailDraftStatus =
  | 'GENERATED'
  | 'EDITED'
  | 'APPROVED'
  | 'CREATED_IN_GMAIL'
  | 'SENT'
  | 'REJECTED';


export interface EmailDraft {

  id: string;

  jobId: string;

  recipientName?: string;

  recipientEmail?: string;

  subject: string;

  body: string;

  status: EmailDraftStatus;

  createdAt: string;

  updatedAt?: string;
}


export interface GenerateEmailRequest {

  jobId: string;

  recipientName?: string;

  recipientEmail?: string;
}


export interface UpdateEmailDraftRequest {

  subject: string;

  body: string;

  recipientName?: string;

  recipientEmail?: string;
}


export interface ApproveEmailResponse {

  approved: boolean;

  draft: EmailDraft;
}


export interface GmailDraftResponse {

  success: boolean;

  gmailDraftId?: string;

  message: string;
}