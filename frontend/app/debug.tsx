// app/(tabs)/debug.tsx
import React, { useEffect, useState } from 'react';
import { View, Text, Button, ScrollView, StyleSheet, Platform, Alert } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import Constants from 'expo-constants';
import { useAuth } from '@/hooks/useAuth';
import { getCurrentUserInfo } from '@/services/userService';
import { clearRememberedCredentials } from '@/services/credentialsService';
import { login } from '@/services/authService';
import { saveTokens, logout as tokenLogout } from '@/services/tokenService';
import { apiFetch } from '@/services/api';

function maskToken(token?: string | null) {
  if (!token) { return 'N/A'; }
  return `${token.slice(0, 4)}...${token.slice(-4)}`;
}

function getTokenExp(token?: string | null) {
  if (!token) { return null; }
  try {
    const [, payload] = token.split('.');
    if (!payload) { return null; }
    const { exp } = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
    if (!exp) { return null; }
    return new Date(exp * 1000).toLocaleString();
  } catch {
    return null;
  }
}

export default function DebugScreen() {
  const { signIn, signOut, isAuthenticated, isLoading } = useAuth();
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [profile, setProfile] = useState<any>(null);

  // Robust app version string
  const appVersion =
    Constants.expoConfig?.version ||
    Constants.manifest?.version ||
    Constants.expoConfig?.runtimeVersion ||
    Constants.nativeAppVersion ||
    'Unknown';

  const reloadData = async () => {
    setAccessToken(await SecureStore.getItemAsync('access_token'));
    setRefreshToken(await SecureStore.getItemAsync('refresh_token'));

    try {
      // Step 1: Get user id from /api/auth/me
      const me = await apiFetch('/api/auth/me') as { id: number; nickname: string };
      // Step 2: Fetch full profile for that id
      const prof = await getCurrentUserInfo();
      setProfile(prof);
    } catch {
      setProfile(null);
    }
  };

  useEffect(() => {
    reloadData();
  }, [isAuthenticated]);

  const handleLogin = async () => {
    const username = 'Rath';
    const password = 'admin';
    try {
      await signIn(username, password);
      Alert.alert('Success', 'Logged in and navigated!');
    } catch (error) {
      handleLoginError(error);
    }
  };

  const handleSimulateLogin = async () => {
    const username = 'Rath';
    const password = 'admin';
    try {
      const data = await login(username, password);
      await saveTokens(data.access_token, data.refresh_token);
      await reloadData();
      Alert.alert('Simulate Login', 'Tokens and profile updated (no navigation).');
    } catch (error) {
      handleLoginError(error);
    }
  };

  const handleClearRemembered = async () => {
    await clearRememberedCredentials();
    await tokenLogout();
    Alert.alert('Credentials Cleared', 'All credentials and tokens have been removed.');
    reloadData();
  };

  function handleLoginError(error: any) {
    console.error('Login Error:', error);
    if (error instanceof Error) {
      Alert.alert('Login Failed', error.message);
    } else {
      Alert.alert(
        'Connection Error',
        'Could not connect to the server. Please check your internet connection and try again.'
      );
    }
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Debug Screen</Text>
      <Text style={styles.header}>Auth Info</Text>
      {/* <Text>isAuthenticated: {String(isAuthenticated)}</Text>
      <Text>isLoading: {String(isLoading)}</Text> */}
      <Text>
        access_token: {maskToken(accessToken)}
        {accessToken && (
          <>
            {'\n'}exp: {getTokenExp(accessToken) || 'N/A'}
          </>
        )}
      </Text>
      <Text>
        refresh_token: {maskToken(refreshToken)}
        {refreshToken && (
          <>
            {'\n'}exp: {getTokenExp(refreshToken) || 'N/A'}
          </>
        )}
      </Text>
      <View style={{ marginTop: 20 }}>
        <Button title="Login (With Navigation)" onPress={handleLogin} disabled={isLoading} />
      </View>
      <View style={{ marginTop: 10 }}>
        <Button title="Simulate Login (No Navigation)" onPress={handleSimulateLogin} disabled={isLoading} />
      </View>
      <View style={{ marginTop: 10 }}>
        <Button title="Logout" onPress={signOut} disabled={isLoading} />
      </View>
      <View style={{ marginTop: 10 }}>
        <Button title="Clear Credentials" onPress={handleClearRemembered} disabled={isLoading} />
      </View>
      <View style={{ marginTop: 20 }}>
        <Button title="Refresh Data" onPress={reloadData} disabled={isLoading} />
      </View>

      <Text style={[styles.header, { marginTop: 30 }]}>Profile Info</Text>
      <Text>
        {profile ? JSON.stringify(profile, null, 2) : 'N/A'}
      </Text>
      <Text style={[styles.header, { marginTop: 30 }]}>Profile Info</Text>
      <Text>
        {profile ? JSON.stringify(profile, null, 2) : 'N/A'}
      </Text>
      <Text style={[styles.header, { marginTop: 30 }]}>App Info</Text>
      <Text>Platform: {Platform.OS}</Text>
      <Text>App Version: {appVersion}</Text>
      <Text>expoConfig.version: {Constants.expoConfig?.version || 'N/A'}</Text>
      <Text>manifest.version: {Constants.manifest?.version || 'N/A'}</Text>
      <Text>nativeAppVersion: {Constants.nativeAppVersion || 'N/A'}</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, alignItems: 'flex-start' },
  title: { fontWeight: 'bold', fontSize: 18, marginBottom: 10 },
  header: { fontWeight: 'bold', marginTop: 20, marginBottom: 6 },
});
