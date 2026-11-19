import { apiClient, supabase } from './client';

export const authApi = {
  login: async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) throw error;
    const res = await apiClient.post('/api/v1/auth/login', { email, password });
    return res.data;
  },
  logout: async () => {
    await supabase.auth.signOut();
    await apiClient.post('/api/v1/auth/logout');
  },
  getMe: async () => {
    const res = await apiClient.get('/api/v1/auth/me');
    return res.data;
  },
};
