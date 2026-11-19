export interface Assessment {
  id: string;
  title: string;
  assessment_number: string;
  assessment_type: 'oral' | 'practical';
  status: string;
  version: number;
  total_marks?: number;
  passing_percentage: number;
  instructions?: string;
  created_at: string;
}

export interface AssessmentTask {
  id: string;
  task_number: number;
  task_title: string;
  task_description?: string;
  max_marks: number;
  task_type: string;
}

export interface ChecklistCriterion {
  id: string;
  task_id?: string;
  criterion_number: string;
  criterion_text: string;
  sub_criterion_text?: string;
  max_marks: number;
  scoring_type: 'binary' | 'numerical' | 'award_max';
  is_sub_total: boolean;
  is_grand_total: boolean;
}

export interface AssessmentSession {
  id: string;
  assessment_id: string;
  trainee_id: string;
  assessor_id: string;
  session_number: number;
  assessment_date?: string;
  assessment_venue?: string;
  total_marks_available: number;
  total_marks_obtained: number;
  percentage_score: number;
  competency_outcome: string;
  assessor_comments?: string;
  feedback_to_candidate?: string;
  status: string;
}

export interface CriterionResult {
  id: string;
  session_id: string;
  criterion_id: string;
  marks_available: number;
  marks_obtained: number;
  is_competent?: boolean;
  assessor_comment?: string;
  evidence_attached: boolean;
}

export interface EvidenceFile {
  id: string;
  original_filename: string;
  system_filename: string;
  file_type: string;
  mime_type: string;
  file_size_bytes: number;
  version: number;
  created_at: string;
}
