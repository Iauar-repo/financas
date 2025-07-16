import { apiFetch } from './api';

export interface UserProfile {
  id: number;
  name?: string;
  username?: string;
  nickname?: string;
  email?: string;
  created_at?: string;
  avatar?: string;
  [key: string]: any;
}

export async function getCurrentUserInfo(): Promise<{ id: number }> {
  return await apiFetch('/api/auth/me');
}

export async function getUserProfile(id: number): Promise<UserProfile> {
  return await apiFetch(`/api/users/${id}`);
}

export async function updateUserProfile(id: number, data: any): Promise<UserProfile> {
  return await apiFetch(`/api/users/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}
