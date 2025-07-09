// hooks/useAuth.ts

import { useContext } from 'react';
import { AuthContext } from '@/contexts/AuthContext';

// Optionally export the context type if it's not already exported
import type { AuthContextProps } from '@/contexts/AuthContext';

export function useAuth(): AuthContextProps {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
}
