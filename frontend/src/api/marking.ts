import { apiClient } from './client';

export const markingApi = {
  recordMarks: (sessionId: string, marks: any[]) => apiClient.post(`/api/v1/marking/sessions/${sessionId}/marks`, marks),
  submit: (sessionId: string, data: any) => apiClient.post(`/api/v1/marking/sessions/${sessionId}/submit`, data),
  getTraineeSessions: (traineeId: string) => apiClient.get(`/api/v1/marking/trainee/${traineeId}/sessions`),
};
