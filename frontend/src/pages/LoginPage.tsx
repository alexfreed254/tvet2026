import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../api/client';
import { useAuthStore } from '../store/authStore';

export function LoginPage() {
  const [email, setEmail] = useState(''); const [password, setPassword] = useState('');
  const [error, setError] = useState(''); const [busy, setBusy] = useState(false);
  const navigate = useNavigate(); const setUser = useAuthStore(s => s.setUser);
  async function submit(e: React.FormEvent) { e.preventDefault(); setBusy(true); setError('');
    try { const { data, error } = await supabase.auth.signInWithPassword({ email, password }); if (error) throw error;
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || ''}/api/v1/auth/me`, { headers: { Authorization: `Bearer ${data.session.access_token}` } });
      if (!response.ok) throw new Error('Your account profile was not found. Ask an administrator to set it up.');
      setUser(await response.json()); navigate('/');
    } catch (err) { setError(err instanceof Error ? err.message : 'Sign in failed'); } finally { setBusy(false); }
  }
  return <main className="min-h-screen grid place-items-center bg-slate-100 p-4"><form onSubmit={submit} className="w-full max-w-md rounded-xl bg-white p-8 shadow space-y-4"><h1 className="text-2xl font-bold">TVET e-ASSESS</h1><p className="text-sm text-slate-500">Digital Practical Assessment Platform</p>{error && <p className="text-sm text-red-600">{error}</p>}<label className="block text-sm">Email<input className="mt-1 w-full border rounded p-2" type="email" required value={email} onChange={e=>setEmail(e.target.value)}/></label><label className="block text-sm">Password<input className="mt-1 w-full border rounded p-2" type="password" required value={password} onChange={e=>setPassword(e.target.value)}/></label><button disabled={busy} className="w-full rounded bg-slate-900 text-white p-2">{busy?'Signing in…':'Sign in'}</button></form></main>;
}
