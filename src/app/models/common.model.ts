export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data: T;
}

export interface Pagination {
  page: number;
  pageSize: number;
  totalItems: number;
  totalPages: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  pagination: Pagination;
}

export interface ApiError {
  statusCode?: number;
  message: string;
  detail?: string;
}

export interface SelectOption<T = string> {
  label: string;
  value: T;
}