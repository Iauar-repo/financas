// app/(tabs)/debug.tsx
import React, { useEffect, useState } from 'react';
import { View, Text, Button, ScrollView, StyleSheet, Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import Constants from 'expo-constants';
import { useAuth } from '@/hooks/useAuth';
import { getUserProfile } from '@/services/userProfileService';
import { clearRememberedCredentials } from '@/services/credentialsService';
import { saveTokens } from '@/services/tokenService';
import { API_URL } from '@/constants/config';
const { signIn } = useAuth();
// This is a debug screen to show authentication and token details.
import { Alert } from 'react-native';
import { login } from '@/services/authService';

export default function DebugScreen() {
  const { signOut, isAuthenticated, isLoading, token } = useAuth();
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [profile, setProfile] = useState<any>(null);
  const [refreshToken2, setRefreshToken2] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      setAccessToken(await SecureStore.getItemAsync('access_token'));
      setRefreshToken(await SecureStore.getItemAsync('refresh_token'));
      try {
        const prof = await getUserProfile();
        setProfile(prof);
      } catch (e) {
        setProfile(null);
      }
    })();
  }, []);

  
const refresh_token2 = 'your_refresh_token_here'; // Use a fixed refresh token for debugging


const handleLogin = async () => {
    // if (!username.trim() || !password.trim()) {
      // Alert.alert('Erro', 'Por favor, preencha todos os campos.');
      const username = 'Rath'; // Use a fixed username for debugging
      const password = 'admin'; // Use a fixed password for debugging
    const data = login(username, password);
    setRefreshToken2(refresh_token2);
    setAccessToken(data.access_Token); // Use a fixed access token for debugging
    
    try {
      await signIn(username, password);

      } catch (error) {
      console.error('Erro de Login:', error);
      if (error instanceof Error) {
        Alert.alert('Falha no Login', error.message);
      } else {
        Alert.alert('Erro de Conexão', 'Não foi possível conectar ao servidor. Verifique sua conexão com a internet e tente novamente.');
      }
    }

      return;
    }
  
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Debug Screen</Text>
      <Text>Platform: {Platform.OS}</Text>
      <Text>App Version: {Constants.manifest?.version || 'N/A'}</Text>
      <Text>API URL: {Constants.expoConfig?.extra?.API_URL || 'N/A'}</Text>
      <Text>isAuthenticated: {String(isAuthenticated)}</Text>
      <Text>isLoading: {String(isLoading)}</Text>
      <Text>access_token: {accessToken?.slice(0, 12)}...{accessToken?.slice(-12)}</Text>
      <Text>refresh_token: {refreshToken2?.slice(0, 12)}...{refreshToken2?.slice(-12)}</Text>
      <Text>User profile: {profile ? JSON.stringify(profile) : 'N/A'}</Text>
      <View style={{ marginTop: 20 }}>
        <Button title="Login" onPress={handleLogin} />
      </View>
      <View style={{ marginTop: 20 }}>
        <Button title="Logout" onPress={signOut} />
      </View>
      <View style={{ marginTop: 10 }}>
        <Button title="Clear Remembered Credentials" onPress={clearRememberedCredentials} />
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, alignItems: 'flex-start' },
  title: { fontWeight: 'bold', fontSize: 18, marginBottom: 10 }
});
