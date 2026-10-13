export type SkillLevel =
  | 'BEGINNER'
  | 'INTERMEDIATE'
  | 'ADVANCED';

export type SkillCategory =
  | 'BACKEND'
  | 'FRONTEND'
  | 'DATABASE'
  | 'AI'
  | 'DEVOPS'
  | 'OTHER';


export interface Skill {

  id?: string;

  name: string;

  level?: SkillLevel;

  category?: SkillCategory;
}


export interface Project {

  id: string;

  title: string;

  description: string;

  technologies: string[];

  projectUrl?: string;

  githubUrl?: string;
}


export interface Experience {

  id: string;

  company: string;

  role: string;

  startDate: string;

  endDate?: string;

  currentlyWorking?: boolean;

  description: string;

  technologies: string[];
}


export interface Education {

  id: string;

  degree: string;

  institute: string;

  startDate?: string;

  endDate?: string;

  cgpa?: string;
}


export interface UserProfile {

  id: string;

  fullName: string;

  email: string;

  phone?: string;

  location?: string;

  headline?: string;

  professionalSummary?: string;

  linkedinUrl?: string;

  githubUrl?: string;

  portfolioUrl?: string;

  skills: Skill[];

  projects: Project[];

  experience: Experience[];

  education: Education[];

  createdAt?: string;

  updatedAt?: string;
}


export interface UpdateProfileRequest {

  fullName: string;

  email: string;

  phone?: string;

  location?: string;

  headline?: string;

  professionalSummary?: string;

  linkedinUrl?: string;

  githubUrl?: string;

  portfolioUrl?: string;

  skills: Skill[];

  projects: Project[];

  experience: Experience[];

  education: Education[];
}