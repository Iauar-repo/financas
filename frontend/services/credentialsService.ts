import * as SecureStore from 'expo-secure-store';

const CREDENTIALS_KEY = 'rememberedCredentials';

interface StoredCredentials {
  username: string;
  password?: string;
}

/**
 * Salva as credenciais do usuário de forma segura.
 * Embora mais seguro que o AsyncStorage, o ideal é salvar apenas o nome de usuário.
 */
export async function saveRememberedCredentials(username: string, password?: string) {
  const credentials = { username, password };
  await SecureStore.setItemAsync(CREDENTIALS_KEY, JSON.stringify(credentials));
}

export async function loadRememberedCredentials(): Promise<StoredCredentials | null> {
  const storedCredentials = await SecureStore.getItemAsync(CREDENTIALS_KEY);
  return storedCredentials ? (JSON.parse(storedCredentials) as StoredCredentials) : null;
}

export async function clearRememberedCredentials() {
  await SecureStore.deleteItemAsync(CREDENTIALS_KEY);
}