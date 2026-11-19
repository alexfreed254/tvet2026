import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';
import { assessmentsApi } from '../../api/assessments';

export function AssessmentCreator() {
  const [form, setForm] = useState({ title: '', assessment_number: '', assessment_type: 'practical', instructions: '', passing_percentage: 50 });
  const [saving, setSaving] = useState(false);

  const handleCreate = async () => {
    setSaving(true);
    try {
      await assessmentsApi.create({ ...form, department_id: '', course_id: '', class_id: '', unit_id: '', academic_period_id: '' });
      alert('Assessment created');
    } finally {
      setSaving(false);
    }
  };

  return (
    <Card>
      <CardHeader><CardTitle>Create New Assessment</CardTitle></CardHeader>
      <CardContent className="space-y-4">
        <div><label className="text-sm font-medium">Title</label><Input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /></div>
        <div><label className="text-sm font-medium">Assessment Number</label><Input value={form.assessment_number} onChange={(e) => setForm({ ...form, assessment_number: e.target.value })} /></div>
        <div><label className="text-sm font-medium">Type</label><select value={form.assessment_type} onChange={(e) => setForm({ ...form, assessment_type: e.target.value })} className="w-full p-2 border rounded"><option value="practical">Practical</option><option value="oral">Oral</option></select></div>
        <div><label className="text-sm font-medium">Passing Percentage</label><Input type="number" value={form.passing_percentage} onChange={(e) => setForm({ ...form, passing_percentage: parseFloat(e.target.value) })} /></div>
        <div><label className="text-sm font-medium">Instructions</label><Textarea value={form.instructions} onChange={(e) => setForm({ ...form, instructions: e.target.value })} rows={4} /></div>
        <Button onClick={handleCreate} disabled={saving}>{saving ? 'Creating...' : 'Create Assessment'}</Button>
      </CardContent>
    </Card>
  );
}
