// services/authService.ts
import { apiFetch } from './api';
import { API_URL } from '@/constants/config';
import { saveTokens } from './tokenService';

// Login no backend
export async function login(username: string, password: string) {
  const res = await fetch(`${API_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.message || 'gay no login');
 
  await saveTokens(data.access_token, data.refresh_token);

  return data;
}


// Registro no backend
export async function register(username: string, email: string, password: string) {
  const res = await fetch(`${API_URL}/api/auth/register`, { // Assumindo que o endpoint é /api/register
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password }),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.message || 'Falha no registro');

  return data;
}

// Valida o token existente
export async function validateToken() {
  // Faz uma chamada para um endpoint protegido.
  // A lógica em `apiFetch` cuidará da renovação do token se necessário.
  // Se a chamada falhar (mesmo após a tentativa de renovação), um erro será lançado.
  // Assumimos um endpoint como /api/me ou /api/validate-token que requer autenticação.
  // Não precisamos dos dados de retorno, apenas que a chamada seja bem-sucedida.
  await apiFetch('/api/access_token', { method: 'GET' });
}
