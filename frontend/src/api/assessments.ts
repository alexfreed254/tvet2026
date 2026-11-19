import { apiClient } from './client';

export const assessmentsApi = {
  list: (params?: Record<string, string>) => apiClient.get('/api/v1/assessments/', { params }),
  get: (id: string) => apiClient.get(`/api/v1/assessments/${id}`),
  create: (data: any) => apiClient.post('/api/v1/assessments/', data),
  addTask: (assessmentId: string, data: any) => apiClient.post(`/api/v1/assessments/${assessmentId}/tasks`, data),
  addCriterion: (assessmentId: string, data: any) => apiClient.post(`/api/v1/assessments/${assessmentId}/criteria`, data),
  publish: (id: string) => apiClient.post(`/api/v1/assessments/${id}/publish`),
  withdraw: (id: string) => apiClient.post(`/api/v1/assessments/${id}/withdraw`),
};
