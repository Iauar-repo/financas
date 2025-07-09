// contexts/AuthContext.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import {
  login as loginService,
  validateToken,
} from '@/services/authService';
import { getToken, logout as logoutService } from '@/services/tokenService';
import { router } from 'expo-router';

export interface AuthContextProps {
  isAuthenticated: boolean;
  isLoading: boolean;
  token: string | null;
  signIn: (username: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextProps>({
  isAuthenticated: false,
  isLoading: true,
  token: null,
  signIn: async () => {},
  signOut: async () => {},
});

export { AuthContext };

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadAuthData = async () => {
      try {
        // validateToken irá lançar um erro se o token for inválido e não puder ser renovado.
        await validateToken();
        // Se a validação for bem-sucedida, um token válido existe no SecureStore.
        const currentToken = await getToken();
        setToken(currentToken);
      } catch (e) {
        // Qualquer erro na validação significa que não estamos autenticados.
        // Garante que estamos deslogados para limpar quaisquer tokens restantes.
        await logoutService();
        setToken(null);
      } finally {
        // Finalizou o carregamento, o app agora pode renderizar a tela correta.
        setIsLoading(false);
      }
    };

    loadAuthData();
  }, []);

  const signIn = async (username: string, password: string) => {
    const data = await loginService(username, password);
    setToken(data.token);
    router.replace('/(tabs)'); // Navega para a área protegida após o login
  };

  const signOut = async () => {
    await logoutService();
    setToken(null);
    router.replace('/login'); // Navega para a tela de login após o logout
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!token,
        isLoading,
        token,
        signIn,
        signOut,
      }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
