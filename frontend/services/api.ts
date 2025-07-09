// services/api.ts
import { getToken, refreshToken, logout } from './tokenService';
import { API_URL } from '@/constants/config';

class ApiError extends Error {
  constructor(message: string, public status: number, public data: any) {
    super(message);
    this.name = 'ApiError';
  }
}

export async function apiFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const doFetch = async (isRetry = false): Promise<Response> => {
    const token = await getToken();

    // Usar a classe Headers é a forma mais segura de manipular cabeçalhos.
    const headers = new Headers(options.headers);
    if (!headers.has('Content-Type')) {
      headers.set('Content-Type', 'application/json');
    }

    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }

    const res = await fetch(`${API_URL}${path}`, {
      ...options,
      headers,
    });

    if (res.status === 401 && !isRetry) {
      try {
        const newToken = await refreshToken();
        if (newToken) {
          // Tenta novamente com o novo token
          return await doFetch(true);
        }
        await logout();
        throw new Error('Sessão expirada. Faça login novamente.');
      } catch (err) {
        await logout();
        const message =
          err instanceof Error
            ? err.message
            : 'Falha ao renovar token. Faça login novamente.';
        throw new Error(message);
      }
    }
    return res;
  };

  try {
    const res = await doFetch();
    const contentType = res.headers.get('content-type');

    if (!res.ok) {
      let errorData: any = null;
      if (contentType?.includes('application/json')) {
        errorData = await res.json();
      }
      const errorMessage =
        errorData?.message || `Erro na requisição: ${res.status} ${res.statusText}`;
      throw new ApiError(errorMessage, res.status, errorData);
    }

    if (res.status === 204 || !contentType?.includes('application/json')) {
      return undefined as T;
    }

    return (await res.json()) as T;
  } catch (error) {
    throw error;
  }
}
