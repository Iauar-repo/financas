
// services/userProfileService.ts
import { apiFetch } from './api';

export async function getUserProfile() {
  return await apiFetch('/api/auth/me');
}

export async function updateUserProfile(profileData: any) {
  return await apiFetch('/api/user/update', {
    method: 'PUT',
    body: JSON.stringify(profileData),
  });
}
