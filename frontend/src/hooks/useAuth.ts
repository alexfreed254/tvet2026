import { useEffect } from 'react';
import { useAuthStore } from '../store/authStore';

export function useAuth() {
  const { user, loading, init, logout } = useAuthStore();
  useEffect(() => { init(); }, []);
  return { user, loading, logout };
}
