import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';

export function ChecklistBuilder({ assessmentId, onAdded }: { assessmentId: string; onAdded: () => void }) {
  const [text, setText] = useState('');
  const [subText, setSubText] = useState('');
  const [maxMarks, setMaxMarks] = useState(0);
  const [scoringType, setScoringType] = useState('numerical');

  const handleAdd = () => {
    console.log('Add criterion:', { criterion_text: text, sub_criterion_text: subText, max_marks: maxMarks, scoring_type: scoringType });
    onAdded();
    setText(''); setSubText(''); setMaxMarks(0);
  };

  return (
    <Card>
      <CardHeader><CardTitle>Add Checklist Criterion</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        <Textarea placeholder="Criterion text" value={text} onChange={(e) => setText(e.target.value)} />
        <Input placeholder="Sub-criterion (e.g., Any 3 x 1)" value={subText} onChange={(e) => setSubText(e.target.value)} />
        <div className="flex gap-2">
          <Input type="number" placeholder="Max marks" value={maxMarks} onChange={(e) => setMaxMarks(parseInt(e.target.value) || 0)} />
          <select value={scoringType} onChange={(e) => setScoringType(e.target.value)} className="border rounded px-3 py-2">
            <option value="numerical">Numerical</option>
            <option value="binary">Binary (1/0)</option>
            <option value="award_max">Award Max</option>
          </select>
        </div>
        <Button onClick={handleAdd}>Add Criterion</Button>
      </CardContent>
    </Card>
  );
}
