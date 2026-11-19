import { useEffect } from 'react';
import { useAssessmentStore } from '../store/assessmentStore';

export function useAssessments(params?: Record<string, string>) {
  const { assessments, loading, fetchAssessments } = useAssessmentStore();
  useEffect(() => { fetchAssessments(params); }, []);
  return { assessments, loading };
}
