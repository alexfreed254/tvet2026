export const COMPETENCY_COLORS: Record<string, string> = {
  competent: 'bg-green-100 text-green-800',
  not_yet_competent: 'bg-red-100 text-red-800',
  proficient: 'bg-blue-100 text-blue-800',
  mastery: 'bg-purple-100 text-purple-800',
  pending: 'bg-gray-100 text-gray-800',
};

export const STATUS_COLORS: Record<string, string> = {
  draft: 'bg-gray-100 text-gray-800',
  published: 'bg-blue-100 text-blue-800',
  in_progress: 'bg-yellow-100 text-yellow-800',
  submitted: 'bg-indigo-100 text-indigo-800',
  approved: 'bg-green-100 text-green-800',
  rejected: 'bg-red-100 text-red-800',
  returned: 'bg-orange-100 text-orange-800',
};

export const USER_ROLES = ['super_admin', 'hod', 'trainer', 'assessor', 'internal_verifier', 'external_verifier', 'trainee', 'management'];
