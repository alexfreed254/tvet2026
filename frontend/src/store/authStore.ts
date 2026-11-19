import { create } from 'zustand';
import { supabase, apiClient } from '../api/client';
import type { User } from '../types/user';

interface AuthState {
  user: User | null;
  loading: boolean;
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  logout: () => Promise<void>;
  init: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: true,
  setUser: (user) => set({ user }),
  setLoading: (loading) => set({ loading }),
  logout: async () => {
    await supabase.auth.signOut();
    set({ user: null });
    window.location.href = '/login';
  },
  init: async () => {
    const { data: { session } } = await supabase.auth.getSession();
    if (session) {
      try {
        const res = await apiClient.get('/api/v1/auth/me');
        set({ user: res.data, loading: false });
      } catch {
        set({ loading: false });
      }
    } else {
      set({ loading: false });
    }
  },
}));
