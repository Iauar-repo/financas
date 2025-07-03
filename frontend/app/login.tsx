import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  ActivityIndicator,
  Platform,
  TouchableOpacity,
} from 'react-native';
import { useRouter } from 'expo-router';

function showAlert(title: string, message: string) {
  if (Platform.OS === 'web') {
    alert(`${title}\n\n${message}`);
  } else {
    // Funciona no celular (Android/iOS)
    import('react-native').then(({ Alert }) => {
      Alert.alert(title, message);
    });
  }
}

export default function LoginScreen() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isPasswordFocused, setIsPasswordFocused] = useState(false);
  const router = useRouter();
  const passwordInputRef = useRef<TextInput>(null);

  const handleLogin = async () => {
    if (!username.trim() || !password.trim()) {
      showAlert('Erro', 'Por favor, preencha todos os campos.');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        router.replace('/');
      } else {
        const errorBody = await response.text();
        try {
          const errorData = JSON.parse(errorBody);
          showAlert('Falha no login', errorData.message || 'Senha ou usuário incorretos.');
        } catch (e) {
          console.error('Server error response (not JSON):', errorBody);
          showAlert('Erro no Servidor', `Ocorreu um erro inesperado (Status: ${response.status}).`);
        }
      }
    } catch (error) {
      console.error('Erro de Conexão:', error);
      showAlert('Erro de Conexão', 'Não foi possível conectar ao servidor. Verifique sua conexão com a internet e tente novamente.');
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
        <View style={styles.passwordContainer}>
          <TextInput
            ref={passwordInputRef}
            style={styles.passwordInput}
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            editable={!isLoading}
            returnKeyType="go"
            onSubmitEditing={handleLogin}
            onFocus={() => setIsPasswordFocused(true)}
            onBlur={() => setIsPasswordFocused(false)}
          />
          {!isPasswordFocused && !password ? (
            <TouchableOpacity
              style={styles.placeholderOverlay}
              activeOpacity={1}
              onPress={() => passwordInputRef.current?.focus()}>
              <Text style={styles.placeholderText}>Senha</Text>
              <Text
                style={styles.forgotPasswordText}
                onPress={() => router.push('/forgot-password')}>
                Esqueci a senha
              </Text>
            </TouchableOpacity>
          ) : null}
        </View>
        <TouchableOpacity
          style={[styles.button, isLoading && styles.buttonDisabled]}
          onPress={handleLogin}
          disabled={isLoading}>
          {isLoading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Entrar</Text>
          )}
        </TouchableOpacity>
        <Text style={styles.signupText}>
          Não tem uma conta?{' '}
          <Text style={styles.signupLink} onPress={() => router.push('/register')}>
            Registrar
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
  passwordContainer: {
    width: '100%',
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    borderRadius: 5,
    marginBottom: 12,
    justifyContent: 'center',
  },
  passwordInput: {
    height: '100%',
    paddingHorizontal: 10,
  },
  placeholderOverlay: {
    position: 'absolute',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    width: '100%',
    paddingHorizontal: 10,
  },
  placeholderText: {
    color: 'gray',
  },
  forgotPasswordText: {
    color: '#007BFF',
    fontWeight: '500',
  },
  button: {
    width: '100%',
    backgroundColor: '#007BFF',
    paddingVertical: 12,
    borderRadius: 5,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonDisabled: {
    backgroundColor: '#A9A9A9',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
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
