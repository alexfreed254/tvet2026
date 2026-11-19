import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { verificationApi } from '../../api/verification';

export function VerificationPanel({ sessionId, onVerified }: { sessionId: string; onVerified: () => void }) {
  const [decision, setDecision] = useState('approved');
  const [comments, setComments] = useState('');
  const [reasons, setReasons] = useState('');

  const handleVerify = async () => {
    try {
      await verificationApi.verify(sessionId, { verifier_type: 'internal', decision, comments, rejection_reasons: reasons });
      onVerified();
    } catch (err: any) { alert(err.response?.data?.detail || 'Verification failed'); }
  };

  return (
    <Card>
      <CardHeader><CardTitle>Verification Decision</CardTitle></CardHeader>
      <CardContent className="space-y-3">
        <select value={decision} onChange={(e) => setDecision(e.target.value)} className="w-full p-2 border rounded">
          <option value="approved">Approve</option>
          <option value="returned_for_correction">Return for Correction</option>
          <option value="rejected">Reject</option>
        </select>
        <Textarea placeholder="Comments" value={comments} onChange={(e) => setComments(e.target.value)} rows={3} />
        {decision !== 'approved' && <Textarea placeholder="Rejection reasons" value={reasons} onChange={(e) => setReasons(e.target.value)} rows={3} />}
        <Button onClick={handleVerify} className="w-full">Submit Verification</Button>
      </CardContent>
    </Card>
  );
}
