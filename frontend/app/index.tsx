
// app/(tabs)/index.tsx
import { Redirect } from 'expo-router';
import { useAuth } from '@/contexts/AuthContext';
import { ActivityIndicator, View } from 'react-native';

export default function Index() {
  const { isLoading, isAuthenticated } = useAuth();

  // Enquanto o AuthContext está verificando o token, mostra uma tela de carregamento.
  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#007BFF" />
      </View>
    );
  }

  // Após o carregamento, redireciona o usuário.
  // Os layouts de `(tabs)` e `(auth)` cuidarão do resto.
  if (isAuthenticated) {
    return <Redirect href="/debug" />; // /tabs aqui
  } else {
    return <Redirect href="/debug" />; // /login aqui
  }
}

