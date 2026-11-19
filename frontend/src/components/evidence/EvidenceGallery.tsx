import { useEffect, useState } from 'react';
import { evidenceApi } from '../../api/evidence';
import type { EvidenceFile } from '../../types/assessment';

export function EvidenceGallery({ sessionId }: { sessionId: string }) {
  const [files, setFiles] = useState<EvidenceFile[]>([]);
  useEffect(() => { evidenceApi.list(sessionId).then((r) => setFiles(r.data)).catch(() => {}); }, [sessionId]);
  if (files.length === 0) return <p className="text-muted-foreground text-sm">No evidence uploaded</p>;
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {files.map((f) => (<div key={f.id} className="border rounded p-3"><p className="text-sm font-medium truncate">{f.original_filename}</p><p className="text-xs text-muted-foreground">{f.file_type} • v{f.version}</p></div>))}
    </div>
  );
}
