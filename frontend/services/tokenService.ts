import * as SecureStore from 'expo-secure-store';
import { API_URL } from '@/constants/config';

export async function saveTokens(access: string, refresh: string | null | undefined) {
  await SecureStore.deleteItemAsync('access_token');
  await SecureStore.deleteItemAsync('refresh_token');

  if (typeof access !== 'string') {
    throw new Error('Invalid access token received.');
  }
  await SecureStore.setItemAsync('access_token', access);

  if (refresh && typeof refresh === 'string') {
    await SecureStore.setItemAsync('refresh_token', refresh);
  } else {
    await SecureStore.deleteItemAsync('refresh_token');
  }
}

export async function getToken(): Promise<string | null> {
  return await SecureStore.getItemAsync('access_token');
}

export async function getRefreshToken(): Promise<string | null> {
  return await SecureStore.getItemAsync('refresh_token');
}

export async function refreshToken(): Promise<string> {
  const refresh = await getRefreshToken();
  if (!refresh) throw new Error('Refresh token missing');

  try {
    const res = await fetch(`${API_URL}/api/auth/refresh`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${refresh}` },
    });

    const data = await res.json();
    if (!res.ok || !data.refresh_token || !data.access_token) {
      throw new Error(data.message || 'Failed to refresh token');
    }

    await saveTokens(data.access_token, data.refresh_token);
    return data.refresh_token;
  } catch (error) {
    throw error;
  }
}

export async function logout() {
  await SecureStore.deleteItemAsync('access_token');
  await SecureStore.deleteItemAsync('refresh_token');
}
