// URL base da API. Vem de EXPO_PUBLIC_API_URL (ver .env.example); o Expo injeta
// variáveis EXPO_PUBLIC_* no bundle em tempo de build. O fallback mantém o app
// rodando em desenvolvimento local caso a variável não esteja definida.
const FALLBACK_API_URL = 'http://192.168.0.20:5000';

export const API_URL = process.env.EXPO_PUBLIC_API_URL ?? FALLBACK_API_URL;
