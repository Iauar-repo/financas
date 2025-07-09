import { Redirect } from 'expo-router';
import { useAuth } from '@/contexts/AuthContext';
import { ActivityIndicator, View } from 'react-native';

/**
 * Este é o ponto de entrada do app.
 * Ele decide qual tela mostrar com base no estado de autenticação.
 */
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
    return <Redirect href="/(tabs)" />;
  } else {
    return <Redirect href="/login" />;
  }
}