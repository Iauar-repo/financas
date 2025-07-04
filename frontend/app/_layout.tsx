import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { useFonts } from 'expo-font';
import { Stack, useRouter, usePathname } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useEffect, useRef, useCallback } from 'react';
import { AppState, PanResponder, View, StyleSheet, AppStateStatus } from 'react-native';
import 'react-native-reanimated';

import { useColorScheme } from '@/hooks/useColorScheme';

// Define o tempo de inatividade em milissegundos
const INACTIVITY_TIMEOUT = 5 * 60 * 1000;

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [loaded] = useFonts({
    SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
  });
  const router = useRouter();
  const pathname = usePathname();
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // --- Lógica de Inatividade ---
  const logout = useCallback(() => {
    // Limpa o timer para evitar execuções múltiplas
    if (timerRef.current) clearTimeout(timerRef.current);
    console.log('Usuário inativo, deslogando...');
    router.replace('/login');
  }, [router]);

  const resetTimer = useCallback(() => {
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(logout, INACTIVITY_TIMEOUT);
  }, [logout]);

  const panResponder = useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => {
        resetTimer();
        return false; // Não "captura" o toque, apenas o detecta
      },
    })
  ).current;

  useEffect(() => {
    const publicRoutes = ['/login', '/forgot-password', '/register'];
    const isAuthenticatedRoute = !publicRoutes.includes(pathname);

    const handleAppStateChange = (nextAppState: AppStateStatus) => {
      if (nextAppState !== 'active' && timerRef.current) {
        clearTimeout(timerRef.current); // Pausa o timer se o app for para o background
      } else if (isAuthenticatedRoute) {
        resetTimer(); // Reinicia o timer se o app voltar ao primeiro plano
      }
    };

    if (isAuthenticatedRoute) {
      resetTimer();
      const subscription = AppState.addEventListener('change', handleAppStateChange);

      return () => {
        subscription.remove();
        if (timerRef.current) clearTimeout(timerRef.current);
      };
    } else if (timerRef.current) {
      clearTimeout(timerRef.current); // Garante que o timer não rode em telas públicas
    }
  }, [pathname, resetTimer]);

  if (!loaded) {
    // Async font loading only occurs in development.
    return null;
  }

  return (
    // O PanResponder envolve toda a aplicação para detectar toques
    <View style={styles.rootContainer} {...panResponder.panHandlers}>
      <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
        <Stack>
          <Stack.Screen name="index" options={{ headerShown: false }} />
          <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
          <Stack.Screen name="login" options={{ headerShown: false }} />
          <Stack.Screen name="forgot-password" options={{ headerShown: false }} />
          <Stack.Screen name="+not-found" />
        </Stack>
        <StatusBar style="auto" />
      </ThemeProvider>
    </View>
  );
}

const styles = StyleSheet.create({
  rootContainer: {
    flex: 1,
  },
});
