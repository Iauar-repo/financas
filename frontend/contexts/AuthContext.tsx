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
  refreshAuth: () => Promise<void>;  // <- ADD THIS
}

const AuthContext = createContext<AuthContextProps>({
  isAuthenticated: false,
  isLoading: true,
  token: null,
  signIn: async () => {},
  signOut: async () => {},
  refreshAuth: async () => {},       // <- ADD THIS
});

export { AuthContext };

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadAuthData = async () => {
      try {
        await validateToken();
        const currentToken = await getToken();
        setToken(currentToken);
      } catch (e) {
        await logoutService();
        setToken(null);
      } finally {
        setIsLoading(false);
      }
    };
    loadAuthData();
  }, []);

  const refreshAuth = async () => {
    const currentToken = await getToken();
    setToken(currentToken);
  };

  const signIn = async (username: string, password: string) => {
    const data = await loginService(username, password);
    setToken(data.access_token); 
    router.replace('/(tabs)');
  };

  const signOut = async () => {
    await logoutService();
    setToken(null);
    router.replace('/login');
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!token,
        isLoading,
        token,
        signIn,
        signOut,
        refreshAuth,     // <- ADD THIS
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
