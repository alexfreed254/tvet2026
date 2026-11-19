import { apiClient } from './client';

export const marksheetApi = {
  generate: (params: Record<string, string>) => apiClient.get('/api/v1/marksheet/generate', { params, responseType: 'blob' }),
  preview: (params: Record<string, string>) => apiClient.get('/api/v1/marksheet/preview', { params }),
};
