import { apiClient } from './client';

export const sessionsApi = {
  list: (params?: Record<string, string>) => apiClient.get('/api/v1/sessions/', { params }),
  create: (assessmentId: string, data: any) => apiClient.post(`/api/v1/sessions/${assessmentId}`, data),
  getSummary: (sessionId: string) => apiClient.get(`/api/v1/marking/sessions/${sessionId}/summary`),
};
