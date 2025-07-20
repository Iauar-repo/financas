import { AuthResponse } from '@/types/api';
import { apiFetch } from './api';
import { saveTokens } from './tokenService';

interface LoginResponse {
  access_token: string;
  refresh_token: string | null;
  [key: string]: any;
}

export async function login(username: string, password: string) {
  const res = await apiFetch<AuthResponse>(
    '/api/auth/login',
    {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    },
    true
  );

  await saveTokens(res.access_token, res.refresh_token);
  return res;
}

export async function register(username: string, email: string, password: string) {
  const res = await apiFetch<AuthResponse>(
    '/api/auth/register',
    {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    },
    true
  );

  return res;
}

export async function validateToken() {
  await apiFetch('/api/access_token', { method: 'GET' });
}
