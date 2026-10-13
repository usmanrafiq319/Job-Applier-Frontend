export type ResumeStatus =
  | 'UPLOADING'
  | 'PROCESSING'
  | 'READY'
  | 'FAILED';


export interface Resume {

  id: string;

  fileName: string;

  fileUrl?: string;

  status: ResumeStatus;

  uploadedAt: string;

  processedAt?: string;

  chunkCount?: number;
}


export interface ResumeUploadResponse {

  resume: Resume;

  message: string;
}


export interface ResumeChunk {

  id: string;

  resumeId: string;

  content: string;

  chunkIndex: number;

  embeddingCreated: boolean;
}