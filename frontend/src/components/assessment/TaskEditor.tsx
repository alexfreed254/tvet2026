import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';

interface TaskEditorProps { assessmentId: string; onTaskAdded: () => void; }

export function TaskEditor({ assessmentId, onTaskAdded }: TaskEditorProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [maxMarks, setMaxMarks] = useState(0);

  const handleAdd = () => {
    console.log('Add task:', { title, description, max_marks: maxMarks });
    onTaskAdded();
    setTitle(''); setDescription(''); setMaxMarks(0);
  };

  return (
    <Card>
      <CardHeader><CardTitle>Add Task</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        <Input placeholder="Task title" value={title} onChange={(e) => setTitle(e.target.value)} />
        <Textarea placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
        <Input type="number" placeholder="Max marks" value={maxMarks} onChange={(e) => setMaxMarks(parseInt(e.target.value) || 0)} />
        <Button onClick={handleAdd}>Add Task</Button>
      </CardContent>
    </Card>
  );
}
