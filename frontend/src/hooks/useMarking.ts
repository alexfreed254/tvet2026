import { useState } from 'react';
import { markingApi } from '../api/marking';

export function useMarking(sessionId: string) {
  const [saving, setSaving] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const saveMarks = async (marks: any[]) => {
    setSaving(true);
    try {
      await markingApi.recordMarks(sessionId, marks);
    } finally {
      setSaving(false);
    }
  };

  const submit = async (data: any) => {
    setSubmitting(true);
    try {
      await markingApi.submit(sessionId, data);
    } finally {
      setSubmitting(false);
    }
  };

  return { saveMarks, submit, saving, submitting };
}
