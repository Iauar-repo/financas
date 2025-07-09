// services/tokenService.ts
import * as SecureStore from 'expo-secure-store';
import { API_URL } from '@/constants/config';

// Salva os tokens
export async function saveTokens(access: string, refresh: string | null | undefined) {
  console.log('Salvando tokens:', { access, refresh });
  if (typeof access !== 'string') {
    // É uma boa prática garantir que o token de acesso seja válido antes de armazenar.
    throw new Error('O token de acesso recebido é inválido.');
  }
  await SecureStore.setItemAsync('access_token', access);

  if (refresh && typeof refresh === 'string') {
    await SecureStore.setItemAsync('refresh_token', refresh);
  } else {
    // Se o refresh token for nulo, indefinido ou não for uma string, remove qualquer um que já exista.
    await SecureStore.deleteItemAsync('refresh_token');
  }
}

// Recupera token atual
export async function getToken(): Promise<string | null> {
  return await SecureStore.getItemAsync('access_token');
}

// Recupera refresh token
export async function getRefreshToken(): Promise<string | null> {
  return await SecureStore.getItemAsync('refresh_token');
}

// Refresh automático
export async function refreshToken(): Promise<string> {
  const refresh = await getRefreshToken();
  if (!refresh) throw new Error('Refresh token ausente');

  const res = await fetch(`${API_URL}/api/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refreshToken: refresh }),
  });

  const data = await res.json();
  if (!res.ok || !data.token) throw new Error(data.message || 'Falha ao renovar token');

  await saveTokens(data.access_token, data.refresh_token);
  return data.token;
}

// Logout (limpa tudo)
export async function logout() {
  await SecureStore.deleteItemAsync('access_token');
  await SecureStore.deleteItemAsync('refresh_token');
}