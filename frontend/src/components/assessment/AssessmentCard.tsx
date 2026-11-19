import { Badge } from '../ui/badge';
import { STATUS_COLORS } from '../../utils/constants';
import { formatDate } from '../../utils/helpers';
import type { Assessment } from '../../types/assessment';

export function AssessmentCard({ assessment, onClick }: { assessment: Assessment; onClick: () => void }) {
  return (
    <div onClick={onClick} className="bg-white border rounded-lg p-4 hover:shadow-md cursor-pointer transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-semibold text-gray-900">{assessment.title}</h3>
        <Badge className={STATUS_COLORS[assessment.status] || ''}>{assessment.status}</Badge>
      </div>
      <p className="text-sm text-gray-600 mb-2">#{assessment.assessment_number} • {assessment.assessment_type.toUpperCase()}</p>
      <div className="flex items-center justify-between text-xs text-gray-500">
        <span>Total: {assessment.total_marks || 0} marks</span>
        <span>{formatDate(assessment.created_at)}</span>
      </div>
    </div>
  );
}
