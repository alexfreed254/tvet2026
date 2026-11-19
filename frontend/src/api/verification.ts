import { apiClient } from './client';

export const verificationApi = {
  verify: (sessionId: string, data: any) => apiClient.post(`/api/v1/verification/sessions/${sessionId}`, data),
  history: (sessionId: string) => apiClient.get(`/api/v1/verification/sessions/${sessionId}/history`),
};
