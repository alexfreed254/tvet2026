import { useState, useRef } from 'react';
import { Card, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Upload, FileImage, FileVideo, FileAudio, FileText, CheckCircle } from 'lucide-react';
import { evidenceApi } from '../../api/evidence';
import type { ChecklistCriterion } from '../../types/assessment';

export function EvidenceUploader({ sessionId, criteria }: { sessionId: string; criteria: ChecklistCriterion[] }) {
  const [selectedCriterion, setSelectedCriterion] = useState('');
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [files, setFiles] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'photo': return <FileImage className="h-5 w-5 text-blue-500" />;
      case 'video': return <FileVideo className="h-5 w-5 text-purple-500" />;
      case 'audio': return <FileAudio className="h-5 w-5 text-orange-500" />;
      default: return <FileText className="h-5 w-5 text-gray-500" />;
    }
  };

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const fileList = event.target.files;
    if (!fileList || fileList.length === 0) return;
    if (!selectedCriterion) { setError('Select a criterion first'); return; }
    setUploading(true); setProgress(0); setError(null);
    for (const file of Array.from(fileList)) {
      try {
        const res = await evidenceApi.upload(sessionId, selectedCriterion, file);
        setFiles((p) => [...p, res.data]);
        setProgress(100);
      } catch (err: any) { setError(err.response?.data?.detail || `Failed: ${file.name}`); }
    }
    setUploading(false);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="space-y-4">
      <div>
        <label className="text-sm font-medium mb-2 block">Select Criterion</label>
        <select value={selectedCriterion} onChange={(e) => setSelectedCriterion(e.target.value)} className="w-full p-2 border rounded-md">
          <option value="">-- Select --</option>
          {criteria.filter((c) => !c.is_sub_total && !c.is_grand_total).map((c) => (<option key={c.id} value={c.id}>{c.criterion_number}. {c.criterion_text}</option>))}
        </select>
      </div>
      <Card className="border-dashed">
        <CardContent className="p-6 text-center">
          <input ref={fileInputRef} type="file" multiple accept="image/*,video/*,audio/*,.pdf,.docx,.xlsx" onChange={handleFileSelect} className="hidden" />
          <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <p className="text-sm text-muted-foreground mb-2">Drag files here or click to browse</p>
          <p className="text-xs text-muted-foreground">JPG, PNG, WEBP, MP4, MOV, WEBM, MP3, WAV, PDF, DOCX, XLSX (Max 100MB)</p>
          <Button onClick={() => fileInputRef.current?.click()} disabled={uploading || !selectedCriterion} className="mt-4"><Upload className="mr-2 h-4 w-4" />Select Files</Button>
        </CardContent>
      </Card>
      {uploading && <div><p className="text-sm mb-1">Uploading... {progress.toFixed(0)}%</p><Progress value={progress} /></div>}
      {error && <p className="text-sm text-red-600">{error}</p>}
      {files.length > 0 && (
        <div className="space-y-2">
          <h3 className="font-medium">Uploaded ({files.length})</h3>
          {files.map((f) => (<div key={f.id} className="flex items-center gap-3 p-3 border rounded-lg">{getFileIcon(f.file_type)}<div className="flex-1 min-w-0"><p className="text-sm font-medium truncate">{f.system_filename}</p><p className="text-xs text-muted-foreground">{f.file_type.toUpperCase()} | {(f.file_size_bytes / 1024).toFixed(1)} KB</p></div><Badge variant="secondary">v{f.version}</Badge><CheckCircle className="h-4 w-4 text-green-500" /></div>))}
        </div>
      )}
    </div>
  );
}
