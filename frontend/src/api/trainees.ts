import { apiClient } from './client';

export const traineesApi = {
  list: (params?: Record<string, string>) => apiClient.get('/api/v1/trainees/', { params }),
  get: (id: string) => apiClient.get(`/api/v1/trainees/${id}`),
  create: (data: any) => apiClient.post('/api/v1/trainees/', data),
};
