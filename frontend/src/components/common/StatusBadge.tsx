import { STATUS_COLORS } from '../../utils/constants';
export function StatusBadge({ status }: { status: string }) { return <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${STATUS_COLORS[status] || 'bg-slate-100 text-slate-700'}`}>{status.replaceAll('_', ' ')}</span>; }
