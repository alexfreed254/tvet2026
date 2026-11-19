import { create } from 'zustand';
import { assessmentsApi } from '../api/assessments';
import type { Assessment } from '../types/assessment';

interface AssessmentState {
  assessments: Assessment[];
  currentAssessment: Assessment | null;
  loading: boolean;
  fetchAssessments: (params?: Record<string, string>) => Promise<void>;
  fetchAssessment: (id: string) => Promise<void>;
}

export const useAssessmentStore = create<AssessmentState>((set) => ({
  assessments: [],
  currentAssessment: null,
  loading: false,
  fetchAssessments: async (params) => {
    set({ loading: true });
    try {
      const res = await assessmentsApi.list(params);
      set({ assessments: res.data, loading: false });
    } catch {
      set({ loading: false });
    }
  },
  fetchAssessment: async (id) => {
    set({ loading: true });
    try {
      const res = await assessmentsApi.get(id);
      set({ currentAssessment: res.data.assessment, loading: false });
    } catch {
      set({ loading: false });
    }
  },
}));
