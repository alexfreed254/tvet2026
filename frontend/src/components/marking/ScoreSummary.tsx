import { Progress } from '../ui/progress';
import { Badge } from '../ui/badge';
import { COMPETENCY_COLORS } from '../../utils/constants';

interface ScoreSummaryProps { obtained: number; available: number; competency: string; passingPercentage: number; }

export function ScoreSummary({ obtained, available, competency, passingPercentage }: ScoreSummaryProps) {
  const percentage = available > 0 ? (obtained / available) * 100 : 0;
  return (
    <div className="space-y-3">
      <div className="grid grid-cols-3 gap-4 text-center">
        <div><p className="text-sm text-muted-foreground">Obtained</p><p className="text-2xl font-bold">{obtained.toFixed(1)}</p></div>
        <div><p className="text-sm text-muted-foreground">Available</p><p className="text-2xl font-bold">{available}</p></div>
        <div><p className="text-sm text-muted-foreground">Percentage</p><p className="text-2xl font-bold">{percentage.toFixed(1)}%</p></div>
      </div>
      <Progress value={percentage} />
      <div className="flex justify-between items-center">
        <span className="text-sm text-muted-foreground">Pass mark: {passingPercentage}%</span>
        <Badge className={COMPETENCY_COLORS[competency] || ''}>{competency?.replace('_', ' ').toUpperCase()}</Badge>
      </div>
    </div>
  );
}
