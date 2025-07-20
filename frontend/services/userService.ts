import { UserInfo } from '@/types/api';
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

/**
 * Fetches current authenticated user info.
 */
export async function getCurrentUserInfo(): Promise<UserInfo> {
  const data = await apiFetch<UserInfo>('/api/auth/me');
  if (!data.id) throw new Error('User ID missing from response.');
  return data;
}

/**
 * Fetches user profile by user ID.
 */
export async function getUserProfile(id: number): Promise<UserProfile> {
  return apiFetch<UserProfile>(`/api/users/${id}`);
}

/**
 * Updates user profile by user ID with partial data.
 */
export async function updateUserProfile(id: number, data: Partial<UserProfile>): Promise<UserProfile> {
  return apiFetch<UserProfile>(`/api/users/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}
