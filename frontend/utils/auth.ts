import * as SecureStore from 'expo-secure-store';

// Salva os tokens
export async function saveTokens(access: string, refresh: string) {
  await SecureStore.setItemAsync("access_token", access);
  await SecureStore.setItemAsync("refresh_token", refresh);
}

// Recupera os tokens
export async function getAccessToken(): Promise<string | null> {
  return await SecureStore.getItemAsync("access_token");
}

export async function getRefreshToken(): Promise<string | null> {
  return await SecureStore.getItemAsync("refresh_token");
}

// Limpa os tokens (logout)
export async function clearTokens() {
  await SecureStore.deleteItemAsync("access_token");
  await SecureStore.deleteItemAsync("refresh_token");
}