import { getToken, refreshToken, logout } from './tokenService';
import { API_URL } from '@/constants/config';

export class ApiError extends Error {
  constructor(message: string, public status: number, public data: any) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Wrapper for fetch API to handle authentication token,
 * refresh logic, and consistent error handling.
 * @template T Expected response type
 */
export async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
  skipAuth = false
): Promise<T> {
  const doFetch = async (isRetry = false): Promise<Response> => {
    let token: string | null = null;
    if (!skipAuth) {
      token = await getToken();
    }

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

    if (res.status === 401 && !isRetry && !skipAuth) {
      try {
        const newToken = await refreshToken();
        if (newToken) {
          return doFetch(true);
        }
        await logout();
        throw new Error('Session expired. Please login again.');
      } catch (err) {
        await logout();
        const message =
          err instanceof Error ? err.message : 'Failed to refresh token. Please login again.';
        throw new Error(message);
      }
    }

    return res;
  };

  const res = await doFetch();

  const contentType = res.headers.get('content-type');

  if (!res.ok) {
    let errorData = null;
    if (contentType?.includes('application/json')) {
      errorData = await res.json();
    }
    const errorMessage = errorData?.message || `Request error: ${res.status} ${res.statusText}`;
    throw new ApiError(errorMessage, res.status, errorData);
  }

  if (res.status === 204 || !contentType?.includes('application/json')) {
    return undefined as T;
  }

  return (await res.json()) as T;
}
