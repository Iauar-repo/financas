// services/userProfileService.ts
import { apiFetch } from './api';

// Fetches the current user's profile using the protected endpoint.
// Returns the user profile object or throws on error.
export async function getUserProfile() {
  return await apiFetch('/api/auth/me'); // Adjust endpoint if needed!
}
