// app/(tabs)/transactions.tsx
import { useEffect } from 'react';
import { View, Text } from 'react-native';
import * as SecureStore from 'expo-secure-store';

export default function TransactionsScreen() {
  useEffect(() => {
    const checkTokens = async () => {
      const accessToken = await SecureStore.getItemAsync('access_token');
      const refreshToken = await SecureStore.getItemAsync('refresh_token');
      console.log('Access Token:', accessToken);
      console.log('Refresh Token:', refreshToken);
    };

    checkTokens();
  }, []);

  return (
    <View>
      <Text>Debug: Check console for token output</Text>
    </View>
  );
}