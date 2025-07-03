import React, { useState, useRef } from 'react';
import { View, Text, StyleSheet, TextInput, Button, Alert, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';

export default function LoginScreen() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const passwordInputRef = useRef<TextInput>(null);

  const handleLogin = async () => {
    // Basic validation
    if (!username.trim() || !password.trim()) {
      Alert.alert('Erro', 'Por favor, preencha o usuário e a senha.');
      return;
    }

    setIsLoading(true);

    try {
      // Note: When running on a physical Android device, 'localhost'
      // must be replaced with your computer's local IP address.
      const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        // On success, navigate to the main app and remove Login from the history.
        router.replace('/(tabs)');
      } else {
        // Handle login failure (e.g., 401 Unauthorized)
        const errorData = await response.json();
        Alert.alert('Falha no Login', errorData.message || 'Credenciais inválidas.');
      }
    } catch (error) {
      console.error('Erro de login:', error);
      Alert.alert('Erro', 'Ocorreu um erro. Verifique sua conexão e tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.formWrapper}>
        <Text style={styles.title}>Login</Text>
        <TextInput
          style={styles.input}
          placeholder="Usuário"
          value={username}
          onChangeText={setUsername}
          autoCapitalize="none"
          editable={!isLoading}
          returnKeyType="next"
          onSubmitEditing={() => passwordInputRef.current?.focus()}
          blurOnSubmit={false}
        />
        <TextInput
          ref={passwordInputRef}
          style={styles.input}
          placeholder="Senha"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          editable={!isLoading}
          returnKeyType="go"
          onSubmitEditing={handleLogin}
        />
        {isLoading ? (
          <ActivityIndicator size="large" color="#0000ff" />
        ) : (
          <Button title="Entrar" onPress={handleLogin} disabled={isLoading} />
        )}
        <Text style={styles.signupText}>
          Não tem uma conta?{' '}
          <Text style={styles.signupLink} onPress={() => router.push('/register')}>
            Cadastre-se
          </Text>
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  formWrapper: {
    width: '80%',
    maxWidth: 400,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  input: {
    width: '100%',
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    borderRadius: 5,
    marginBottom: 12,
    paddingHorizontal: 10,
  },
  signupText: {
    marginTop: 20,
    color: 'gray',
    fontSize: 16,
  },
  signupLink: {
    color: '#007BFF',
    fontWeight: 'bold',
  },
});