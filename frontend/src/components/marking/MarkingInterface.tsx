import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Alert, AlertDescription } from '../ui/alert';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../ui/table';
import { CheckCircle, Save, Send } from 'lucide-react';
import { sessionsApi } from '../../api/sessions';
import { markingApi } from '../../api/marking';
import { EvidenceUploader } from '../evidence/EvidenceUploader';
import { COMPETENCY_COLORS } from '../../utils/constants';
import type { ChecklistCriterion } from '../../types/assessment';

export function MarkingInterface({ sessionId }: { sessionId: string }) {
  const [session, setSession] = useState<any>(null);
  const [criteria, setCriteria] = useState<ChecklistCriterion[]>([]);
  const [results, setResults] = useState<Record<string, any>>({});
  const [comments, setComments] = useState<Record<string, string>>({});
  const [assessorComments, setAssessorComments] = useState('');
  const [feedback, setFeedback] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [tab, setTab] = useState<'checklist' | 'evidence' | 'comments'>('checklist');

  useEffect(() => { loadSession(); }, [sessionId]);

  const loadSession = async () => {
    try {
      const res = await sessionsApi.getSummary(sessionId);
      setSession(res.data);
      setCriteria(res.data.criteria_results || []);
      const resultsMap: Record<string, any> = {};
      (res.data.criteria_results || []).forEach((cr: any) => { resultsMap[cr.criterion_id] = cr; if (cr.comment) setComments((p) => ({ ...p, [cr.criterion_id]: cr.comment })); });
      setResults(resultsMap);
      setAssessorComments(res.data.assessor_comments || '');
      setFeedback(res.data.feedback_to_candidate || '');
    } catch (err: any) { setError(err.response?.data?.detail || 'Failed to load'); }
  };

  const handleMarkChange = (criterionId: string, value: number, maxMarks: number) => {
    if (value < 0) value = 0;
    if (value > maxMarks) value = maxMarks;
    setResults((p) => ({ ...p, [criterionId]: { ...(p[criterionId] || {}), marks_obtained: value, marks_available: maxMarks } }));
  };

  const saveMarks = async () => {
    const marks = Object.entries(results).map(([cid, r]: [string, any]) => ({ criterion_id: cid, marks_obtained: r.marks_obtained || 0, assessor_comment: comments[cid] || undefined }));
    try {
      await markingApi.recordMarks(sessionId, marks);
      setSuccess('Marks saved');
      setTimeout(() => setSuccess(null), 3000);
    } catch (err: any) { setError(err.response?.data?.detail || 'Failed to save'); }
  };

  const submit = async () => {
    if (!window.confirm('Submit for verification?')) return;
    try {
      await markingApi.submit(sessionId, { assessor_comments: assessorComments, feedback_to_candidate: feedback });
      setSuccess('Submitted for verification');
    } catch (err: any) { setError(err.response?.data?.detail || 'Failed to submit'); }
  };

  if (!session) return <div className="p-8 text-center">Loading...</div>;

  const totalObtained = Object.values(results).reduce((s: number, r: any) => s + (r.marks_obtained || 0), 0);
  const totalAvailable = session.total_marks_available || 0;
  const percentage = totalAvailable > 0 ? (totalObtained / totalAvailable) * 100 : 0;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Assessment Session</h1>
          <p className="text-muted-foreground">Session #{session.session_number}</p>
        </div>
        <Badge className={COMPETENCY_COLORS[session.competency_outcome] || ''}>{session.competency_outcome?.replace('_', ' ').toUpperCase()}</Badge>
      </div>

      <Card>
        <CardContent className="pt-6">
          <div className="grid grid-cols-4 gap-4">
            <div className="text-center"><p className="text-sm text-muted-foreground">Obtained</p><p className="text-2xl font-bold">{totalObtained.toFixed(1)}</p></div>
            <div className="text-center"><p className="text-sm text-muted-foreground">Available</p><p className="text-2xl font-bold">{totalAvailable}</p></div>
            <div className="text-center"><p className="text-sm text-muted-foreground">Percentage</p><p className="text-2xl font-bold">{percentage.toFixed(1)}%</p></div>
            <div className="text-center"><p className="text-sm text-muted-foreground">Pass Mark</p><p className="text-2xl font-bold">{session.passing_percentage || 50}%</p></div>
          </div>
          <Progress value={percentage} className="mt-4" />
        </CardContent>
      </Card>

      {success && <Alert className="bg-green-50 border-green-200"><CheckCircle className="h-4 w-4 text-green-600" /><AlertDescription className="text-green-800">{success}</AlertDescription></Alert>}
      {error && <Alert variant="destructive"><AlertDescription>{error}</AlertDescription></Alert>}

      <div className="flex gap-2 border-b">
        {(['checklist', 'evidence', 'comments'] as const).map((t) => (
          <button key={t} onClick={() => setTab(t)} className={`px-4 py-2 text-sm font-medium ${tab === t ? 'border-b-2 border-primary' : 'text-muted-foreground'}`}>{t.charAt(0).toUpperCase() + t.slice(1)}</button>
        ))}
      </div>

      {tab === 'checklist' && (
        <Card>
          <CardHeader><CardTitle>Observation Checklist</CardTitle></CardHeader>
          <CardContent>
            <Table>
              <TableHeader><TableRow><TableHead className="w-[40%]">Item</TableHead><TableHead className="w-[15%] text-center">Available</TableHead><TableHead className="w-[20%] text-center">Obtained</TableHead><TableHead className="w-[25%]">Comments</TableHead></TableRow></TableHeader>
              <TableBody>
                {criteria.map((c: any) => (
                  <TableRow key={c.criterion_id}>
                    <TableCell><p className="font-medium">{c.criterion_text}</p>{c.sub_criterion_text && <p className="text-sm text-muted-foreground italic">({c.sub_criterion_text})</p>}</TableCell>
                    <TableCell className="text-center font-medium">{c.max_marks}</TableCell>
                    <TableCell className="text-center"><Input type="number" min={0} max={c.max_marks} value={results[c.criterion_id]?.marks_obtained || 0} onChange={(e) => handleMarkChange(c.criterion_id, parseFloat(e.target.value) || 0, c.max_marks)} className="w-20 mx-auto text-center" /></TableCell>
                    <TableCell><Input placeholder="Comment" value={comments[c.criterion_id] || ''} onChange={(e) => setComments((p) => ({ ...p, [c.criterion_id]: e.target.value }))} /></TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}

      {tab === 'evidence' && <Card><CardHeader><CardTitle>Multimedia Evidence</CardTitle></CardHeader><CardContent><EvidenceUploader sessionId={sessionId} criteria={criteria} /></CardContent></Card>}

      {tab === 'comments' && (
        <Card>
          <CardHeader><CardTitle>Comments & Submit</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            <div><label className="text-sm font-medium">Assessor Comments</label><Textarea value={assessorComments} onChange={(e) => setAssessorComments(e.target.value)} rows={4} /></div>
            <div><label className="text-sm font-medium">Feedback to Candidate</label><Textarea value={feedback} onChange={(e) => setFeedback(e.target.value)} rows={4} /></div>
            <div className="flex gap-4">
              <Button onClick={saveMarks} variant="outline"><Save className="mr-2 h-4 w-4" />Save Progress</Button>
              <Button onClick={submit} className="bg-green-600 hover:bg-green-700"><Send className="mr-2 h-4 w-4" />Submit for Verification</Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
