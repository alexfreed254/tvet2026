import { apiClient } from './client';

export const evidenceApi = {
  upload: (sessionId: string, criterionId: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post(`/api/v1/evidence/upload/${sessionId}?criterion_id=${criterionId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  list: (sessionId: string, criterionId?: string) => apiClient.get(`/api/v1/evidence/session/${sessionId}`, { params: { criterion_id: criterionId } }),
  download: (evidenceId: string) => apiClient.get(`/api/v1/evidence/download/${evidenceId}`),
};
